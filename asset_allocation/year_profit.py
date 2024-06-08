import numpy as np

class YearProfit():
    def __init__(self, transactions):
        self.transactions = transactions
    def sales(self):
        transactions_df = self.transactions.value()
        external_transactions = transactions_df.dropna(subset=['execution_center'])
        return external_transactions[external_transactions['local_value'] > 0]
    def sales_by_year(self, year: int):
        df = self.sales()
        return df[df.datetime.dt.year.eq(year)]
    def transactions_queue(self):
        return self.transactions.queue()
