# transactions/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Transaction
from decimal import Decimal

class TransactionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='pass')
        self.client.force_authenticate(self.user)

    def test_transaction_list(self):
        Transaction.objects.create(user=self.user, amount=100, txn_type='deposit')
        resp = self.client.get('/api/transactions/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_transaction_summary(self):
        Transaction.objects.create(user=self.user, amount=100, txn_type='deposit')
        Transaction.objects.create(user=self.user, amount=-40, txn_type='withdraw')
        resp = self.client.get('/api/transactions/summary/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('total_credits', resp.data)
        self.assertIn('total_debits', resp.data)
        self.assertEqual(float(resp.data['total_credits']), 100.0)
        self.assertEqual(float(resp.data['total_debits']), 40.0)

    def test_transaction_filtering_by_type(self):
        Transaction.objects.create(user=self.user, amount=200, txn_type='deposit')
        Transaction.objects.create(user=self.user, amount=-50, txn_type='withdraw')
        resp = self.client.get('/api/transactions/?search=withdraw')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['txn_type'], 'withdraw')
