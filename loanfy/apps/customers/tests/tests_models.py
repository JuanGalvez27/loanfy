from apps.customers.models import Customer
from django.test import TestCase
from django.utils import timezone


class CustomerModelTests(TestCase):
    def setUp(self):
        """Configura datos para los tests"""
        self.customer = Customer.objects.create(
            external_id="cust123", status=1, score=750.00
        )

    def test_customer_creation(self):
        """Test que asegura que el Customer se crea correctamente"""
        self.assertEqual(self.customer.external_id, "cust123")
        self.assertEqual(self.customer.status, 1)
        self.assertEqual(self.customer.score, 750.00)
        self.assertIsInstance(self.customer.created_at, timezone.datetime)
        self.assertIsInstance(self.customer.updated_at, timezone.datetime)

    def test_string_representation(self):
        """Test que asegura que la representación en string del Customer es correcta"""
        self.assertEqual(str(self.customer), str(self.customer.id))
