class Customer:
    def __init__(self, name, customer_id, email):
        self.name, self.customer_id = name, customer_id
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, v):
        if '@' not in v: raise ValueError(f"Некорректный email: {v}")
        self._email = v

    def to_dict(self):
        return {"name": self.name, "customer_id": self.customer_id, "email": self.email}

    @staticmethod
    def from_dict(d):
        return Customer(d["name"], d["customer_id"], d["email"])

    def __str__(self):
        return f"{self.name}, {self.email}"