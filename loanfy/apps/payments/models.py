import uuid

from apps.choices import PAYMENT_STATUS_CHOICES, payment_status_dict
from apps.customers.models import Customer
from django.db import models


class Payment(models.Model):
    id = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        help_text="Payment ID",
    )
    external_id = models.CharField(
        max_length=60, unique=True, help_text="External payment ID"
    )
    total_amount = models.DecimalField(
        max_digits=20, decimal_places=10, help_text="Amout of the payment"
    )
    status = models.SmallIntegerField(
        choices=PAYMENT_STATUS_CHOICES, help_text="Status of the payment"
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.external_id
