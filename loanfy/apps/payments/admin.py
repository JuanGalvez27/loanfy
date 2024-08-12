from apps.payments.models import Payment, PaymentDetail
from django.contrib import admin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentDetail)
class PaymentDetailAdmin(admin.ModelAdmin):
    pass
