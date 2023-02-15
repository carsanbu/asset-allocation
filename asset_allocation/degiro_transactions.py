import pandas as pd

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


