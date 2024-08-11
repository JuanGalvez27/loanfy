from apps.customers.views import CustomerCreateAPIView, CustomerDetailAPIView
from django.urls import path

urlpatterns = [
    path("create/", CustomerCreateAPIView.as_view(), name="create_customer"),
    path(
        "detail/<str:external_id>/",
        CustomerDetailAPIView.as_view(),
        name="detail_customer",
    ),
]
