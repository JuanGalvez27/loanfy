from apps.loans.models import Loan
from django.contrib import admin


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    pass
