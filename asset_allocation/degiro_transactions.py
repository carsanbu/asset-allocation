import pandas as pd
from asset_allocation.transaction import Price
from asset_allocation.transactions_queue import TransactionsQueue, TransactionPacket

class TransactionsQueueSet:
    def __init__(self):
        self.queue_set = set()
    def add(self, item: TransactionsQueue):
        self.queue_set.add(item)
    def get(self, isin: str):
        for item in self.queue_set:
            if item.isin == isin:
                return item
        return None

class DegiroESTransactions:
    def __init__(self, transactions):
        self.transactions = transactions
    def value(self):
        datetime = self.transactions['Hora'] + ' ' + self.transactions['Fecha']
        transactions = self.transactions.copy()
        transactions.insert(0, 'date', pd.to_datetime(datetime, format='%H:%M %d-%m-%Y'))
        transactions = transactions.drop('Fecha', axis=1)
        transactions = transactions.drop('Hora', axis=1)
        transactions = transactions.set_index('date')
        transactions = transactions.rename(columns={
            'Producto': 'product',
            'Bolsa de': 'exchange',
            'Centro de ejecución': 'execution_center',
            'Número': 'number',
            'Precio': 'price',
            'Unnamed: 8': 'price_currency',
            'Valor local': 'local_value',
            'Unnamed: 10': 'local_currency',
            'Valor': 'value',
            'Unnamed: 12': 'currency',
            'Tipo de cambio': 'exchange_rate',
            'Costes de transacción': 'transaction_fees',
            'Unnamed: 15': 'transaction_fees_currency',
            'Total': 'total',
            'Unnamed: 17': 'total_currency',
            'ID Orden': 'id'
        })
        return transactions
    def queue(self):
        df = self.value()
        queue_set = TransactionsQueueSet()

        for index, row in df.iloc[::-1].iterrows():
            queue_set.add(TransactionsQueue(row.ISIN))
            transactions_queue = queue_set.get(row.ISIN)
            transactions_queue.put(TransactionPacket(row.number,
                Price(row.value, row.currency), row.total))
        return transactions_queue


