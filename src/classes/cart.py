from logger_config import logger


class Cart:
    def __init__(self, customer):
        self.customer, self.items = customer, {}

    def add_item(self, product, quantity):
        if quantity <= 0: raise ValueError("Количество должно быть положительным")
        total = self.items.get(product.product_id, 0) + quantity
        if not product.is_available(total):
            return False
        self.items[product.product_id] = total
        logger.info(f"Корзина [{self.customer.name}]: +{quantity} × {product.name}")
        return True

    def remove_item(self, product_id):
        if product_id not in self.items: return False
        del self.items[product_id]
        return True

    def update_quantity(self, product_id, new_qty):
        if product_id not in self.items: return False
        if new_qty <= 0: del self.items[product_id]
        else: self.items[product_id] = new_qty
        return True

    def get_total_price(self, catalog):
        return round(sum(catalog[pid].price * qty
                         for pid, qty in self.items.items() if pid in catalog), 2)

    def clear(self):
        self.items.clear()

    def __str__(self):
        if not self.items: return f"Корзина [{self.customer.name}]: пуста"
        lines = [f"  ID={pid}, кол-во: {q}" for pid, q in self.items.items()]
        return f"Корзина [{self.customer.name}]:\n" + "\n".join(lines)