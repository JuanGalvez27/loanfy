from apps.customers.models import Customer
from rest_framework import serializers
from rest_framework.validators import ValidationError


class CustomerWriteSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    score = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_external_id(self, value):
        customers = Customer.objects.all().values_list("external_id")
        if value in customers:
            raise ValidationError(self.external_id, 400)
        return value


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return_dict = {
            "id": rep["id"],
            "external_id": rep["external_id"],
            "status": rep["status"],
            "score": rep["score"],
            "preapproved_at": rep["created_at"],
        }
        return return_dict
