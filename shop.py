import json
from logger_config import logger
from product import Product, DigitalProduct
from customer import Customer
from cart import Cart
from order import Order


class Shop:
    def __init__(self):
        self.products, self.customers = {}, {}
        self.orders, self.carts = [], {}
        self._next_id = 1

    def __len__(self):
        return len(self.products)

    def __getitem__(self, key):
        if isinstance(key, int): return list(self.products.values())[key]
        return self.products[key]

    def add_product(self, p):
        self.products[p.product_id] = p
        logger.info(f"Товар добавлен: {p}")

    def register_customer(self, c):
        self.customers[c.customer_id] = c
        logger.info(f"Покупатель: {c}")

    def get_cart(self, customer):
        if customer.customer_id not in self.carts: self.carts[customer.customer_id] = Cart(customer)
        return self.carts[customer.customer_id]

    def create_order(self, customer, payment_processor=None):
        cart = self.get_cart(customer)
        if not cart.items: return None

        for pid, qty in cart.items.items():
            if pid not in self.products or not self.products[pid].is_available(qty): return None

        total = cart.get_total_price(self.products)

        for pid, qty in cart.items.items():
            if not isinstance(self.products[pid], DigitalProduct): self.products[pid].quantity -= qty

        order = Order(self._next_id, customer, cart.items, total)
        self._next_id += 1
        self.orders.append(order)
        cart.clear()
        logger.info(f"Заказ создан: {order}")

        if payment_processor and payment_processor.process_payment(order, total):
            order.update_status("оплачен")

        return order

    def find_products_by_name(self, name):
        return [p for p in self.products.values() if name.lower() in p.name.lower()]

    def display_products(self):
        for p in self.products.values(): print(p)

    def save_to_json(self, path="shop_data.json"):
        data = {"products": [p.to_dict() for p in self.products.values()],
                "customers": [c.to_dict() for c in self.customers.values()],
                "orders": [o.to_dict() for o in self.orders],
                "next_id": self._next_id}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Сохранено в {path}")

    def load_from_json(self, path="shop_data.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.products = {p.product_id: p for p in map(Product.from_dict, data.get("products", []))}
        self.customers = {c.customer_id: c for c in map(Customer.from_dict, data.get("customers", []))}
        self.orders = []
        for od in data.get("orders", []):
            c = self.customers.get(od["customer_id"], Customer("?", od["customer_id"], "?@?.?"))
            o = Order(od["order_id"], c, od["items"], od["total_price"])
            o.status = od["status"]
            self.orders.append(o)
        self._next_id = data.get("next_id", 1)
        logger.info(f"Загружено из {path}")