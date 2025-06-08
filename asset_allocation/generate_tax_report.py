from asset_allocation.year_profit import YearProfit
from asset_allocation.degiro_transactions import DegiroESTransactions
import pandas as pd

if __name__ == '__main__':
    year = 2024
    file = 'data/Transactions2025.csv'
    transactions = DegiroESTransactions(pd.read_csv(file))
    profit = YearProfit(transactions)
    print(f'Sales in the {year}:')
    print(profit.sales_by_year(year))
    print('Transactions:')
    profit.transactions_queue()
