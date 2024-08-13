from apps.customers.models import Customer
from apps.loans.models import Loan
from apps.payments.models import Payment, PaymentDetail
from django.test import TestCase
from django.utils import timezone


class PaymentModelTests(TestCase):
    def setUp(self):
        """Configura datos para los tests"""
        self.customer = Customer.objects.create(
            external_id="cust123", status=1, score=750.00
        )
        self.payment = Payment.objects.create(
            external_id="pay123",
            total_amount=500.00,
            status=1,
            paid_at=timezone.now(),
            customer=self.customer,
        )

    def test_payment_creation(self):
        """Test que asegura que el Payment se crea correctamente"""
        self.assertEqual(self.payment.external_id, "pay123")
        self.assertEqual(self.payment.total_amount, 500.00)
        self.assertEqual(self.payment.status, 1)
        self.assertIsInstance(self.payment.paid_at, timezone.datetime)
        self.assertEqual(self.payment.customer, self.customer)

    def test_string_representation(self):
        """Test que asegura que la representación en string del Payment es correcta"""
        self.assertEqual(str(self.payment), str(self.payment.id))


class PaymentDetailModelTests(TestCase):
    def setUp(self):
        """Configura datos para los tests"""
        self.customer = Customer.objects.create(
            external_id="cust123", status=1, score=750.00
        )
        self.loan = Loan.objects.create(
            external_id="loan123",
            amount=1000.00,
            outstanding=1000.00,
            status=1,
            maximum_payment_date=timezone.now() + timezone.timedelta(days=30),
            customer=self.customer,
        )
        self.payment = Payment.objects.create(
            external_id="pay123",
            total_amount=500.00,
            status=1,
            paid_at=timezone.now(),
            customer=self.customer,
        )
        self.payment_detail = PaymentDetail.objects.create(
            amount=200.00, loan=self.loan, payment=self.payment
        )

    def test_payment_detail_creation(self):
        """Test que asegura que el PaymentDetail se crea correctamente"""
        self.assertEqual(self.payment_detail.amount, 200.00)
        self.assertEqual(self.payment_detail.loan, self.loan)
        self.assertEqual(self.payment_detail.payment, self.payment)

    def test_string_representation(self):
        """Test que asegura que la representación en string del PaymentDetail es correcta"""
        self.assertEqual(str(self.payment_detail), str(self.payment_detail.id))
