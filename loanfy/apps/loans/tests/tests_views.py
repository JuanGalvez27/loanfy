from apps.customers.models import Customer
from apps.loans.models import Loan
from apps.users.models import User
from apps.utils import view_url
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class LoanAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="mail@test.com", password="testpass"
        )
        self.client = Client()
        self.token = RefreshToken.for_user(self.user).access_token
        self.client = Client(headers={"Authorization": "Bearer " + str(self.token)})
        self.customer = Customer.objects.create(
            external_id="cust123", status=1, score=75000.00
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
        self.valid_data = {
            "external_id": "loan456",
            "amount": 50.00,
            "outstanding": 50.00,
            "status": 1,
            "contract_version": "v2",
            "maximum_payment_date": "2024-12-31T01:17:54.955Z",
            "customer": str(self.customer.id),
        }
        self.invalid_data = {
            "external_id": "",
            "amount": "invalid_amount",
            "outstanding": -500.00,
            "status": 999,
            "contract_version": "",
            "maximum_payment_date": "invalid_date",
            "customer": "invalid_customer",
        }
        self.loan_create_url = view_url("create_loan")
        self.loan_detail_url = view_url(
            "detail_loan", {"external_id": str(self.loan.external_id)}
        )
        self.loan_list_url = view_url("list_loans")
        self.loan_no_existent_id = view_url(
            "balance_customer", {"external_id": "not_existent"}
        )

    def test_create_loan(self):
        response = self.client.post(self.loan_create_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["external_id"], self.valid_data["external_id"])
        self.assertEqual(response.data["amount"], str(self.valid_data["amount"]) + "0")

    def test_create_loan_invalid_data(self):
        response = self.client.post(self.loan_create_url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_loan_detail(self):
        response = self.client.get(self.loan_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["external_id"], self.loan.external_id)

    def test_get_loan_detail_not_found(self):
        response = self.client.get(self.loan_no_existent_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_loan(self):
        update_data = {
            "amount": "1000.00",
            "contract_version": "v3",
        }
        response = self.client.patch(self.loan_detail_url, json=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], str(update_data["amount"]))

    def test_list_loans(self):
        response = self.client.get(
            self.loan_list_url, {"customer_external_id": self.customer.external_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_loans_no_filter(self):
        response = self.client.get(self.loan_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
