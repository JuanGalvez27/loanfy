from apps.customers.models import Customer
from apps.loans.models import Loan
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone


class LoanModelTests(TestCase):
    def setUp(self):
        # Configura datos para los tests
        self.customer = Customer.objects.create(external_id="cust123", score=1000000)
        self.loan = Loan.objects.create(
            external_id="loan123",
            amount=1000.00,
            outstanding=1000.00,
            status=1,
            maximum_payment_date=timezone.now() + timezone.timedelta(days=30),
            customer=self.customer,
        )

    def test_loan_creation(self):
        """Test que asegura que el Loan se crea correctamente"""
        self.assertEqual(self.loan.external_id, "loan123")
        self.assertEqual(self.loan.amount, 1000.00)
        self.assertEqual(self.loan.outstanding, 1000.00)
        self.assertEqual(self.loan.status, 1)
        self.assertIsInstance(self.loan.maximum_payment_date, timezone.datetime)
        self.assertEqual(self.loan.customer, self.customer)

    def test_set_outstanding(self):
        """Test que asegura que el método set_outstanding funciona correctamente"""
        self.loan.set_outstanding(500.00)
        self.assertEqual(self.loan.outstanding, 500.00)

        # Verifica si se lanza una excepción cuando el valor excede el outstanding
        with self.assertRaises(ValidationError):
            self.loan.set_outstanding(600.00)

    def test_get_customer_balance(self):
        """Test que asegura que el método get_customer_balance calcula correctamente el saldo del cliente"""
        # Crea más préstamos para el mismo cliente
        Loan.objects.create(
            external_id="loan124",
            amount=500.00,
            outstanding=500.00,
            status=1,
            maximum_payment_date=timezone.now() + timezone.timedelta(days=30),
            customer=self.customer,
        )
        loan = Loan()
        balance = loan.get_customer_balance(self.customer)
        self.assertEqual(balance, 1500.00)  # Suma de los préstamos creados

    def test_string_representation(self):
        """Test que asegura que la representación en string del Loan es correcta"""
        self.assertEqual(str(self.loan), str(self.loan.id))
