from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple

@dataclass
class Price():
    price: float
    price_currency: str
    def __repr__(self):
        return f'{self.price} {self.price_currency}'

class Transaction():
    def __init__(self, number: int, price: Price, total: float, date: datetime = None, order_id: str = None):
        self.number = number
        self.price = price
        self.total = total
        self.date = date
        self.order_id = order_id
    def __repr__(self):
        return f'{self.number}\t{self.price}\t{self.date}\t{self.order_id}'
    def value_per_transaction(self):
        """This value is counting commissions on the purchase and sales."""
        return self.total / self.number
    def is_same_value(self, transaction):
        return transaction.number == self.number and transaction.price == self.price and transaction.total == self.total

