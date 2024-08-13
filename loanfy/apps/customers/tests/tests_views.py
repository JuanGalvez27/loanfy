from apps.customers.models import Customer
from apps.loans.models import Loan
from apps.users.models import User
from apps.utils import view_url
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class CustomerAPITests(APITestCase):
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
        self.valid_customer_data = {"external_id": "cust456", "score": "800000.00"}
        self.invalid_customer_data = {"external_id": "", "score": "invalid_score"}

        self.customer_create_url = view_url("create_customer")
        self.customer_list_url = view_url("list_customers")
        self.customer_detail_url = view_url(
            "detail_customer", {"external_id": str(self.customer.external_id)}
        )
        self.customer_balance_url = view_url(
            "balance_customer", {"external_id": str(self.customer.external_id)}
        )
        self.customer_no_existent_id = view_url(
            "balance_customer", {"external_id": "not_existent"}
        )

    def test_create_customer(self):
        response = self.client.post(
            self.customer_create_url, data=self.valid_customer_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["external_id"], self.valid_customer_data["external_id"]
        )
        self.assertEqual(response.data["score"], str(self.valid_customer_data["score"]))

    def test_create_customer_invalid_data(self):
        response = self.client.post(
            self.customer_create_url, self.invalid_customer_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_customers(self):
        response = self.client.get(self.customer_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_customer_detail(self):
        response = self.client.get(self.customer_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["external_id"], self.customer.external_id)

    def test_get_customer_detail_not_found(self):
        response = self.client.get(self.customer_no_existent_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_customer_balance(self):
        response = self.client.get(self.customer_balance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["external_id"], self.customer.external_id)
        self.assertEqual(response.data["total_debt"], "1000.00")
        self.assertEqual(
            response.data["available_amount"], str(self.customer.score - 1000.00) + "0"
        )

    def test_get_customer_balance_not_found(self):
        response = self.client.get(self.customer_no_existent_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
