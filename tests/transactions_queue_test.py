import unittest
from asset_allocation.transaction import Price, Transaction
from asset_allocation.transactions_queue import TransactionsQueue

class TransactionsQueueTest(unittest.TestCase):
    def test_1_put(self):
        transactions_queue = TransactionsQueue('xxx')
        transaction = Price(200, 'EUR')
        transactions_queue.put(Transaction(5, transaction, 1200))
        first_2_transactions = transactions_queue.get(2)[0]
        self.assertTrue(first_2_transactions.is_same_value(Transaction(2, transaction, 480)))

        second_2_transactions = transactions_queue.get(2)[0]
        self.assertTrue(second_2_transactions, Transaction(2, transaction, 480))

        self.assertRaises(IndexError, transactions_queue.get, 2)

    def test_2_put(self):
        transactions_queue = TransactionsQueue('xxx')
        price1 = Price(200, 'EUR')
        price2 = Price(400, 'EUR')
        transactions_queue.put(Transaction(5, price1, 1200))
        transactions_queue.put(Transaction(10, price2, 4000))

        first_6_transactions = transactions_queue.get(6)
        self.assertTrue(first_6_transactions[0].is_same_value(Transaction(5, price1, 1200)))
        self.assertTrue(first_6_transactions[1].is_same_value(Transaction(1, price2, 400)))

        second_2_transactions = transactions_queue.get(2)[0]
        self.assertTrue(second_2_transactions.is_same_value(Transaction(2, price2, 800)))

    def test_3_put(self):
        transactions_queue = TransactionsQueue('xxx')
        price1 = Price(200, 'EUR')
        price2 = Price(400, 'EUR')
        transactions_queue.put(Transaction(5, price1, 1200))
        transactions_queue.put(Transaction(10, price2, 4000))

        first_6_transactions = transactions_queue.get(6)
        self.assertTrue(first_6_transactions[0].is_same_value(Transaction(5, price1, 1200)))
        self.assertTrue(first_6_transactions[1].is_same_value(Transaction(1, price2, 400)))

        second_2_transactions = transactions_queue.get(4)[0]
        self.assertTrue(second_2_transactions.is_same_value(Transaction(4, price2, 1600)))

    def test_4_put(self):
        transactions_queue = TransactionsQueue('xxx')
        price1 = Price(200, 'EUR')
        price2 = Price(400, 'EUR')
        transactions_queue.put(Transaction(5, price1, 1200))
        transactions_queue.put(Transaction(10, price2, 4000))

        first_6_transactions = transactions_queue.get(6)
        self.assertTrue(first_6_transactions[0].is_same_value(Transaction(5, price1, 1200)))
        self.assertTrue(first_6_transactions[1].is_same_value(Transaction(1, price2, 400)))

        self.assertRaises(IndexError, transactions_queue.get, 10)
if __name__ == '__main__':
    unittest.main()
