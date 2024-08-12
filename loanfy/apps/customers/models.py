import uuid

from apps.choices import CUSTOMER_STATUS_CHOICES
from django.db import models


class Customer(models.Model):
    id = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        help_text="Customer ID",
    )
    external_id = models.CharField(
        max_length=60, unique=True, help_text="External Customer ID"
    )
    status = models.SmallIntegerField(
        choices=CUSTOMER_STATUS_CHOICES, default=1, help_text="Status of the customer"
    )
    score = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount that can be used to apply for loans",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def get_customer_balance(self):
        pass
