from apps.customers.models import Customer
from apps.loans.models import Loan
from apps.payments.models import Payment
from apps.users.models import User
from apps.utils import view_url
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class PaymentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="mail@test.com", password="testpass"
        )
        self.client = Client()
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = Client(headers={"Authorization": "Bearer " + str(self.token)})
        self.customer = Customer.objects.create(
            external_id="cust123", status=1, score=750.00
        )
        self.loan = Loan.objects.create(
            external_id="loan123",
            amount=1000.00,
            outstanding=1000.00,
            status=1,
            contract_version="v1",
            maximum_payment_date="2024-08-13T01:17:54.955Z",
            customer=self.customer,
        )
        self.payment = Payment.objects.create(
            external_id="payment123",
            total_amount=500.00,
            status=1,
            customer=self.customer,
        )

        self.valid_payment_data = {
            "external_id": "payment_01",
            "total_amount": "100",
            "customer": str(self.customer.id),
            "loan": str(self.loan.id),
        }
        self.invalid_payment_data = {
            "external_id": "",
            "total_amount": "invalid_amount",
            "customer": "invalid_uuid",
            "loan": "invalid_uuid",
        }
        self.payment_create_url = view_url("create_payment")
        self.payment_list_url = view_url("list_payment")

    def test_create_payment(self):
        response = self.client.post(self.payment_create_url, self.valid_payment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)

    def test_create_payment_invalid(self):
        response = self.client.post(
            self.payment_create_url,
            self.invalid_payment_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("external_id", response.data)

    def test_list_payments(self):
        response = self.client.get(
            self.payment_list_url, {"customer_external_id": self.customer.external_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["external_id"], self.payment.external_id)
