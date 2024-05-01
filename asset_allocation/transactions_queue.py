from asset_allocation.transaction import Transaction
from typing import NamedTuple

class TransactionPacket(NamedTuple):
    number: int
    transaction: Transaction
    total: float
    def __repr__(self):
        return f'{self.number} {self.transaction}'
    def value_per_transaction(self):
        """This value is counting commissions on the purchase and sales."""
        return self.total / self.number

class TransactionsQueue():
    def __init__(self):
        self.transaction_list = []
    def __repr__(self):
        return str(self.transaction_list)

    def put(self, transaction_packet: TransactionPacket) -> None:
        self.transaction_list.append(transaction_packet)

    def get(self, number: int) -> list[TransactionPacket]:
        packet_list = []
        first_item = self.transaction_list[0]
        remaining_transactions = number
        while remaining_transactions > 0:
            if first_item.number > remaining_transactions:
                packet_list.append(
                    TransactionPacket(
                        remaining_transactions,
                        first_item.transaction,
                        remaining_transactions*first_item.value_per_transaction()))
                new_number = first_item.number - remaining_transactions
                self.transaction_list[0] = TransactionPacket(
                        new_number,
                        first_item.transaction,
                        new_number*first_item.value_per_transaction())
                remaining_transactions = 0
            else:
                remaining_transactions = remaining_transactions - first_item.number
                packet_list.append(self.transaction_list.pop(0))
                if len(self.transaction_list) ==  0 and remaining_transactions > 0:
                    raise IndexError("Not enough items in the queue.")
                first_item = self.transaction_list[0]
        return packet_list
