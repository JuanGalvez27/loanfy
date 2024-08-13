from apps.loans.views import LoanCreateAPIView, LoanDetailAPIView, LoanListAPIView
from django.urls import path

urlpatterns = [
    path("create/", LoanCreateAPIView.as_view(), name="create_loan"),
    path("list/", LoanListAPIView.as_view(), name="list_loans"),
    path(
        "detail/<str:external_id>/",
        LoanDetailAPIView.as_view(),
        name="detail_loan",
    ),
    path(
        "customer/<str:customer_external_id>/",
        LoanDetailAPIView.as_view(),
        name="loans_by_customer",
    ),
]
