from logger_config import logger


class Order:
    STATUSES = ("новый", "оплачен", "отправлен", "доставлен")

    def __init__(self, order_id, customer, items, total_price):
        self.order_id, self.customer = order_id, customer
        self.items, self.total_price = dict(items), total_price
        self.status = "новый"

    def update_status(self, new):
        if new not in self.STATUSES:
            raise ValueError(f"Недопустимый статус: {new}")
        if self.STATUSES.index(new) != self.STATUSES.index(self.status) + 1:
            raise ValueError(f"Нельзя: {self.status} → {new}")
        self.status = new
        logger.info(f"Заказ #{self.order_id}: → {new}")

    def to_dict(self):
        return {"order_id": self.order_id, "customer_id": self.customer.customer_id,
                "items": self.items, "total_price": self.total_price, "status": self.status}

    def __str__(self):
        return f"Заказ #{self.order_id} | {self.customer.name} | {self.total_price} руб. | {self.status}"