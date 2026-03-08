from product import Product, DigitalProduct, DiscountedProduct
from customer import Customer
from payment import CreditCardProcessor, PayPalProcessor
from shop import Shop


if __name__ == "__main__":
    shop = Shop()

    shop.add_product(Product("Продукт А", 55000, 10, "P001"))
    shop.add_product(Product("Продукт Б", 1500, 50, "P002"))
    shop.add_product(DigitalProduct("Продукт В", 1990, 999999, "P003", 350, "example.com"))
    shop.add_product(DiscountedProduct("Продукт Г", 6000, 20, "P004", 25))

    shop.display_products()
    print(f"Всего товаров: {len(shop)}")
    print(f"По индексу: {shop[0]}")
    print(f"По ID: {shop['P004']}\n")

    c = Customer("Анна", "C001", "ex@mail.ru")
    shop.register_customer(c)

    cart = shop.get_cart(c)
    cart.add_item(shop["P001"], 1)
    cart.add_item(shop["P003"], 2)
    cart.add_item(shop["P004"], 3)
    print(cart)
    print(f"Итого: {cart.get_total_price(shop.products)} руб.\n")

    order = shop.create_order(c, CreditCardProcessor("4276 **** 7890"))
    print(order)

    order.update_status("отправлен")
    order.update_status("доставлен")
    print(order)

    shop.save_to_json()
    print('Корзина сохранена')