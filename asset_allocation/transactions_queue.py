from asset_allocation.transaction import Price, Transaction

class TransactionsQueue():
    def __init__(self, isin):
        self.isin = isin
        self.transaction_list = []
    def __repr__(self):
        return str(self.transaction_list)

    def put(self, transaction: Transaction) -> None:
        self.transaction_list.append(transaction)

    def get(self, number: int) -> list[Transaction]:
        packet_list = []
        first_item = self.transaction_list[0]
        remaining_transactions = number
        while remaining_transactions > 0:
            if first_item.number > remaining_transactions:
                packet_list.append(
                    Transaction(
                        remaining_transactions,
                        first_item.price,
                        remaining_transactions*first_item.value_per_transaction()))
                new_number = first_item.number - remaining_transactions
                self.transaction_list[0] = Transaction(
                        new_number,
                        first_item.price,
                        new_number*first_item.value_per_transaction())
                remaining_transactions = 0
            else:
                remaining_transactions = remaining_transactions - first_item.number
                packet_list.append(self.transaction_list.pop(0))
                if len(self.transaction_list) ==  0 and remaining_transactions > 0:
                    raise IndexError("Not enough items in the queue.")
                first_item = self.transaction_list[0]
        return packet_list
