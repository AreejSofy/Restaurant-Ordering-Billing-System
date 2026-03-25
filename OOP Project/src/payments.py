# src/payments.py
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount): pass

class CashPayment(Payment):
    def __init__(self, cash_given):
        self.cash_given = cash_given
    def pay(self, amount):
        if self.cash_given < amount:
            return False, f"Insufficient Cash. Need {amount - self.cash_given:.2f} EGP more."
        return True, f"Cash Payment Successful!\nChange: {self.cash_given - amount:.2f} EGP"

class CardPayment(Payment):
    def __init__(self, card_number):
        self.card_number = card_number
    def pay(self, amount):
        masked = "**** **** **** " + self.card_number[-4:]
        return True, f"Card {masked} charged {amount:.2f} EGP successfully."