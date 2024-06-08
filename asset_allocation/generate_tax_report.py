from asset_allocation.year_profit import YearProfit
from asset_allocation.degiro_transactions import DegiroESTransactions
import pandas as pd

if __name__ == '__main__':
    transactions = DegiroESTransactions(pd.read_csv('data/Transactions3.csv'))
    profit = YearProfit(transactions)
    print(profit.sales_by_year(2023))
    profit.transactions_queue()
