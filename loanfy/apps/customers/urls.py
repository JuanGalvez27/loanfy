from apps.customers.views import (
    CustomerBalanceAPIView,
    CustomerCreateAPIView,
    CustomerDetailAPIView,
    CustomerListAPIView,
)
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("create/", CustomerCreateAPIView.as_view(), name="create_customer"),
    path("list/", CustomerListAPIView.as_view(), name="list_customers"),
    path(
        "detail/<str:external_id>/",
        CustomerDetailAPIView.as_view(),
        name="detail_customer",
    ),
    path(
        "balance/<str:external_id>/",
        CustomerBalanceAPIView.as_view(),
        name="balance_customer",
    ),
]
