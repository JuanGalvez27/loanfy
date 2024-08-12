from datetime import timezone

from apps.choices import LOAN_STATUS_CHOICES, loan_status_dict
from apps.customers.models import Customer
from apps.loans.models import Loan
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.validators import ValidationError


class LoanUpdateSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    taken_at = serializers.DateTimeField()


class LoanSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    outstanding = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    customer = serializers.UUIDField()
    taken_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Loan
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return_data = {
            "external_id": rep["external_id"],
            "customer_external_id": instance.customer.external_id,
            "amount": rep["amount"],
            "outstanding": rep["outstanding"],
            "status": rep["status"],
        }
        return return_data

    def total_outstanding(self):
        total_outstanding = Loan.objects.filter(
            customer=self.validated_data["customer"]
        ).aggregate(total=Sum("outstanding"))["total"]
        if not total_outstanding:
            total_outstanding = 0
        return total_outstanding

    def validate_outstanding(self, value):
        customer_score = Customer.objects.get(id=self.validated_data["customer"]).score
        if ((float(self.total_outstanding())) + float(value)) > customer_score:
            raise ValidationError(
                {
                    "outstanding": "The total of the customer's loans is greater than their Score"
                }
            )
        return value

    def create(self, validated_data):
        customer = Customer.objects.get(id=validated_data["customer"])
        outstanding = validated_data["amount"]
        validated_outstanding = self.validate_outstanding(outstanding)
        validated_data["outstanding"] = validated_outstanding
        validated_data["customer"] = customer
        return Loan.objects.create(**validated_data)

    def update(self, instance, validated_data):

        return super().update(instance, validated_data)
