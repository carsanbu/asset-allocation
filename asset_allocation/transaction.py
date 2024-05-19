from dataclasses import dataclass

@dataclass
class Price():
    price: float
    price_currency: str
    def __repr__(self):
        return f'{self.price} {self.price_currency}'
