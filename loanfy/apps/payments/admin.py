from apps.payments.models import Payment
from django.contrib import admin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
