import uuid

from apps.choices import LOAN_STATUS_CHOICES, loan_status_dict
from apps.customers.models import Customer
from django.core.exceptions import ValidationError
from django.db import models


class Loan(models.Model):
    id = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        help_text="Loan ID",
    )
    external_id = models.CharField(
        max_length=60, unique=True, help_text="External if of the Loan"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Amount with which the loan was created",
    )
    outstanding = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Total amount of customer loans"
    )
    status = models.SmallIntegerField(
        choices=LOAN_STATUS_CHOICES, default=1, help_text="Status of the loan"
    )
    contract_version = models.CharField(
        blank=True,
        default="",
        max_length=255,
        help_text="Optional field that can contain any value",
    )
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField(
        null=True, blank=True, help_text="Date when the loan is activated"
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def set_outstanding(self, value):
        self.outstanding = float(self.outstanding) - float(value)
        if self.outstanding < 0:
            raise ValidationError(
                "The value of the payment is greater than the outstanding"
            )
        return self.save()

    def get_customer_balance(self, customer):
        loans = self.__class__.objects.filter(customer=customer).values_list(
            "outstanding", flat=True
        )
        total_outstanding = sum(list(loans))
        return total_outstanding
