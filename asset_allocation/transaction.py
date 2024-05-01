from dataclasses import dataclass

@dataclass
class Transaction():
    isin: str
    price: float
    price_currency: str
    def __repr__(self):
        return f'{self.isin}: {self.price} {self.price_currency}'
