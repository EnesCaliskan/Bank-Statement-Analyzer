from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from io import StringIO
from .models import Transaction

class TransactionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.upload_url = reverse('upload-csv')
        self.kpi_url = reverse('kpi-summary')

    def test_csv_upload_success(self):
        """Test if we can upload a valid CSV file"""
        csv_content = (
            "date,amount,currency,description,type\n"
            "2025-07-01,1000.00,TRY,Salary,credit\n"
            "2025-07-02,-200.00,TRY,Rent,debit"
        )
        
        file_obj = StringIO(csv_content)
        file_obj.name = "test.csv"

        response = self.client.post(self.upload_url, {'file': file_obj}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_duplicate_prevention(self):
        """Test that uploading the same file twice fails (Idempotency)"""
        csv_content = "date,amount,currency,description,type\n2025-07-01,500,TRY,Test,credit"
        
        file1 = StringIO(csv_content)
        file1.name = "test.csv"
        self.client.post(self.upload_url, {'file': file1}, format='multipart')

        file2 = StringIO(csv_content)
        file2.name = "test.csv"
        response = self.client.post(self.upload_url, {'file': file2}, format='multipart')
        
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_kpi_calculations(self):
        Transaction.objects.create(user=self.user, date='2025-01-01', amount=1000, description="Income", transaction_type='credit', unique_hash='hash1')
        Transaction.objects.create(user=self.user, date='2025-01-02', amount=-300, description="Rent", transaction_type='debit', unique_hash='hash2')

        response = self.client.get(self.kpi_url)
        
        data = response.json()
        self.assertEqual(data['total_income'], 1000.00)
        self.assertEqual(data['total_expense'], -300.00)
        self.assertEqual(data['net_cash_flow'], 700.00)