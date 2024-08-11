from apps.customers.views import CustomerCreateAPIView, CustomerDetailAPIView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("create/", CustomerCreateAPIView.as_view(), name="create_customer"),
    path(
        "detail/<str:external_id>/",
        CustomerDetailAPIView.as_view(),
        name="detail_customer",
    ),
]
