class Product:
    def __init__(self, name, price, quantity, product_id):
        self.name, self.product_id = name, product_id
        self.price, self.quantity = price, quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, v):
        if v <= 0: raise ValueError("Цена должна быть положительной")
        self._price = v

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, v):
        if v < 0: raise ValueError("Количество не может быть отрицательным")
        self._quantity = v

    def is_available(self, n):
        return self.quantity >= n

    def to_dict(self):
        return {"type": "Product", "name": self.name, "price": self.price,
                "quantity": self.quantity, "product_id": self.product_id}

    @staticmethod
    def from_dict(d):
        t = d.get("type", "Product")
        if t == "DigitalProduct":
            return DigitalProduct(d["name"], d["price"], d.get("quantity", 999999),
                                  d["product_id"], d["file_size"], d["download_link"])
        if t == "DiscountedProduct":
            return DiscountedProduct(d["name"], d["original_price"], d["quantity"],
                                     d["product_id"], d["discount_percent"])
        return Product(d["name"], d["price"], d["quantity"], d["product_id"])

    def __str__(self):
        return f"[{self.product_id}] {self.name} — {self.price} руб., {self.quantity} шт."


class DigitalProduct(Product):
    def __init__(self, name, price, quantity, product_id, file_size, download_link):
        super().__init__(name, price, quantity, product_id)
        self.file_size, self.download_link = file_size, download_link

    def is_available(self, n=1):
        return True

    def to_dict(self):
        d = super().to_dict()
        d.update(type="DigitalProduct", file_size=self.file_size,
                 download_link=self.download_link)
        return d

    def __str__(self):
        return (f"[{self.product_id}] {self.name} — {self.price} руб., "
                f"{self.file_size} МБ, {self.download_link}")


class DiscountedProduct(Product):
    def __init__(self, name, price, quantity, product_id, discount_percent):
        self.discount_percent = discount_percent
        super().__init__(name, price, quantity, product_id)

    @property
    def price(self):
        return round(self._price * (1 - self.discount_percent / 100), 2)

    @price.setter
    def price(self, v):
        if v <= 0: raise ValueError("Цена должна быть положительной")
        self._price = v

    @property
    def original_price(self):
        return self._price

    def to_dict(self):
        return {"type": "DiscountedProduct", "name": self.name,
                "original_price": self.original_price, "quantity": self.quantity,
                "product_id": self.product_id, "discount_percent": self.discount_percent}

    def __str__(self):
        return (f"[{self.product_id}] {self.name} — {self.price} руб. "
                f"(-{self.discount_percent}%, было {self.original_price}), {self.quantity} шт.")