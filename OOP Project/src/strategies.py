from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def apply(self, total): pass
    @abstractmethod
    def label(self): pass

class NoDiscount(Discount):
    def apply(self, total): return total
    def label(self): return "No discount"

class PercentageDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent
    def apply(self, total):
        return total * (1 - self.percent / 100)
    def label(self):
        return f"{self.percent}% off"

class FixedDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount
    def apply(self, total):
        return max(0, total - self.amount)
    def label(self):
        return f"{self.amount} EGP off"

DISCOUNT_MAP = {
    "SAVE20" : PercentageDiscount(20),
    "WELCOME": PercentageDiscount(10),
    "FLAT50" : FixedDiscount(50),
}

def get_discount(code):
    return DISCOUNT_MAP.get(code.strip().upper(), NoDiscount())