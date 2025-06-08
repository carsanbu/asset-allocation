import pandas as pd
import numpy as np
from asset_allocation.transaction import Price, Transaction
from asset_allocation.transactions_queue import TransactionsQueue

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
        transactions.insert(0, 'datetime', pd.to_datetime(datetime, format='%H:%M %d-%m-%Y', errors='raise'))
        transactions = transactions.drop('Fecha', axis=1)
        transactions = transactions.drop('Hora', axis=1)
        transactions = transactions.rename(columns={
            'Producto': 'product',
            'Bolsa de': 'exchange',
            'Centro de': 'execution_center', # ejecución
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
            'ID Orden': 'order_id',
        })
        return transactions
    def queue(self):
        df = self.value()
        cleaned_transactions = df.dropna(subset=['datetime'])
        external_transactions = cleaned_transactions # df.dropna(subset=['execution_center'])
        queue_set = TransactionsQueueSet()


        for index, row in external_transactions.iloc[::-1].iterrows():
            transactions_queue = queue_set.get(row.ISIN)
            if row['number'] > 0: # Purchase
                if transactions_queue is None:
                    queue_set.add(TransactionsQueue(row.ISIN))
                    transactions_queue = queue_set.get(row.ISIN)
                purchase = Transaction(row.number,
                    Price(row.value, row.currency),
                    row.total, row.datetime, row.order_id)
                transactions_queue.put(purchase)
                #print('Purchased:\t', row.ISIN, purchase)
                #print('amount: ', transactions_queue.amount())
            elif row['number'] < 0: # Sell
                if transactions_queue is None:
                    raise RuntimeError('Cannot find the transaction queue')
                sold_number = -row.number
                sold_list = transactions_queue.get(sold_number)
                print(str(row.datetime) + " " + row.ISIN + ": " + row['product'])
                print('Sell: ', sold_number,  row.total)
                accum_benefit = 0
                for sold in sold_list:
                    print('\t', sold)
                    benefit = (row.value/sold_number)*sold.number + sold.total
                    accum_benefit = accum_benefit + benefit
                    print(f'\tBenefit: {benefit} {(benefit/(-sold.total))*100:0.0f}%') # Because sold is negative
                print("Total benefit:", accum_benefit)
                print("--------------------------------------------")
                #print('amount: ', transactions_queue.amount())
            else:
                print("Error: local value 0")


