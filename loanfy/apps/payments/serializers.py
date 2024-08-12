import uuid

from apps.loans.models import Loan
from apps.payments.models import Payment, PaymentDetail
from django.core.exceptions import ValidationError as error
from rest_framework import serializers
from rest_framework.validators import ValidationError


class CreatePaymentSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    customer = serializers.UUIDField()
    loan = serializers.UUIDField()

    def validate_loan(self, value):
        loans = list(Loan.objects.all().values_list("id", flat=True))
        loans = [str(loan) for loan in loans]
        if str(value) in loans:
            return value
        raise ValidationError(f"Loan with id {value} do not exists", 400)


class PaymentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentDetail
        fields = "__all__"

    def create(self, validated_data):
        loan = Loan.objects.get(id=str(validated_data["loan"]))
        loan.set_outstanding(validated_data["amount"])
        return PaymentDetail.objects.create(**validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Payment
        fields = "__all__"

    def create(self, validated_data):

        new_payment = Payment.objects.create(**validated_data)
        loan = Loan.objects.get(id=self.context.get("loan"))
        payment_detail_data = {}
        payment_detail_data["payment"] = new_payment.id
        payment_detail_data["amount"] = validated_data["total_amount"]
        payment_detail_data["loan"] = loan.id
        payment_detail_serializer = PaymentDetailSerializer(data=payment_detail_data)
        payment_detail_serializer.is_valid(raise_exception=True)
        if payment_detail_serializer.is_valid():
            try:
                payment_detail_serializer.save()
                return new_payment
            except error as e:
                new_payment.delete()
                raise ValidationError({"message": e}, 400)


class PaymentListSerializer(PaymentSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return_data = {
            "id": rep["id"],
            "external_id": rep["external_id"],
            "customer_external_id": self.context.get("customer_external_id"),
            # “loan_external_id”: “loan-01”,
            "payment_date": rep["created_at"],
            # 'status': 1
            "total_amount": rep["total_amount"],
            # 'payment_amount': 500
        }
        return return_data
