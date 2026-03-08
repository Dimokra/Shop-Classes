from abc import ABC, abstractmethod
from logger_config import logger


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, order, amount): pass


class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card="**** 1234"):
        self.card = card

    def process_payment(self, order, amount):
        logger.info(f"Карта {self.card}: заказ #{order.order_id}, {amount} руб.")
        return True


class PayPalProcessor(PaymentProcessor):
    def __init__(self, email="user@paypal.com"):
        self.pp_email = email

    def process_payment(self, order, amount):
        logger.info(f"PayPal {self.pp_email}: заказ #{order.order_id}, {amount} руб.")
        return True