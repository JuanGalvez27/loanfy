from apps.payments.views import PaymentCreateAPIView, PaymentListAPIView
from django.urls import path

urlpatterns = [
    path("create/", PaymentCreateAPIView.as_view(), name="create_payment"),
    path("list/", PaymentListAPIView.as_view(), name="list_payment"),
    # path(
    #     "detail/<str:external_id>/",
    #     CustomerDetailAPIView.as_view(),
    #     name="detail_customer",
    # ),
]
