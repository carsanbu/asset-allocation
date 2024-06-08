import unittest
from asset_allocation.degiro_transactions import DegiroESTransactions
from io import StringIO
import pandas as pd

class DegiroESTransactionsTest(unittest.TestCase):
    transactions_csv = """Fecha,Hora,Producto,ISIN,Bolsa de,Centro de ejecución,Número,Precio,,Valor local,,Valor,,Tipo de cambio,Costes de transacción,,Total,,ID Orden
11-02-2022,15:32,ISHARES MSCI WOR A,IE00B4L5Y983,EAM,XAMS,8,70.6000,EUR,-264.80,EUR,-264.80,EUR,,,,-264.80,EUR,3fe53aaf-c330-4e18-a06a-31f1ed79f08c
10-02-2022,18:00,UNITEDHEALTH GROUP INC,US91324P1021,NSY,XNAS,1,283.5000,USD,-283.50,USD,-250.44,EUR,1.0734,-1.00,EUR,-251.44,EUR,26912c8c-71d9-4c79-94ff-4f426d67b8e2"""
    def test(self):
        transactions_df = pd.read_csv(StringIO(self.transactions_csv))
        transactions = DegiroESTransactions(transactions_df)
        transactions_parsed = transactions.value()
        print(transactions_parsed.head())
        self.assertEqual(transactions_parsed.price[1], 283.5)

    def test_queue(self):
        transactions_df = pd.read_csv(StringIO(self.transactions_csv))
        transactions = DegiroESTransactions(transactions_df)
        print(transactions.queue())
if __name__ == '__main__':
    unittest.main()
