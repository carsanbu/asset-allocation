import unittest
from asset_allocation.transaction import Transaction
from asset_allocation.transactions_queue import TransactionsQueue, TransactionPacket

class TransactionsQueueTest(unittest.TestCase):
    def test_1_put(self):
        transactions_queue = TransactionsQueue()
        transaction = Transaction('xxxxxx', 200, 'EUR')
        transactions_queue.put(TransactionPacket(5, transaction, 1200))
        first_2_transactions = transactions_queue.get(2)[0]
        self.assertEqual(first_2_transactions, TransactionPacket(2, transaction, 480))

        second_2_transactions = transactions_queue.get(2)[0]
        self.assertEqual(second_2_transactions, TransactionPacket(2, transaction, 480))

        self.assertRaises(IndexError, transactions_queue.get, 2)

    def test_2_put(self):
        transactions_queue = TransactionsQueue()
        transaction = Transaction('xxxxxx', 200, 'EUR')
        transaction2 = Transaction('xxxxxy', 400, 'EUR')
        transactions_queue.put(TransactionPacket(5, transaction, 1200))
        transactions_queue.put(TransactionPacket(10, transaction2, 4000))

        first_6_transactions = transactions_queue.get(6)
        self.assertEqual(first_6_transactions[0], TransactionPacket(5, transaction, 1200))
        self.assertEqual(first_6_transactions[1], TransactionPacket(1, transaction2, 400))

        second_2_transactions = transactions_queue.get(2)[0]
        self.assertEqual(second_2_transactions, TransactionPacket(2, transaction2, 800))

    def test_3_put(self):
        transactions_queue = TransactionsQueue()
        transaction = Transaction('xxxxxx', 200, 'EUR')
        transaction2 = Transaction('xxxxxy', 400, 'EUR')
        transactions_queue.put(TransactionPacket(5, transaction, 1200))
        transactions_queue.put(TransactionPacket(10, transaction2, 4000))

        first_6_transactions = transactions_queue.get(6)
        self.assertEqual(first_6_transactions[0], TransactionPacket(5, transaction, 1200))
        self.assertEqual(first_6_transactions[1], TransactionPacket(1, transaction2, 400))

        second_2_transactions = transactions_queue.get(4)[0]
        self.assertEqual(second_2_transactions, TransactionPacket(4, transaction2, 1600))

    def test_4_put(self):
        transactions_queue = TransactionsQueue()
        transaction = Transaction('xxxxxx', 200, 'EUR')
        transaction2 = Transaction('xxxxxy', 400, 'EUR')
        transactions_queue.put(TransactionPacket(5, transaction, 1200))
        transactions_queue.put(TransactionPacket(10, transaction2, 4000))

        first_6_transactions = transactions_queue.get(6)
        self.assertEqual(first_6_transactions[0], TransactionPacket(5, transaction, 1200))
        self.assertEqual(first_6_transactions[1], TransactionPacket(1, transaction2, 400))

        self.assertRaises(IndexError, transactions_queue.get, 10)
if __name__ == '__main__':
    unittest.main()
