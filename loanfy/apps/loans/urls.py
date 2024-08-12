from apps.loans.views import LoanCreateAPIView, LoanDetailAPIView, LoanListlAPIView
from django.urls import path

urlpatterns = [
    path("create/", LoanCreateAPIView.as_view(), name="create_loan"),
    path("list/", LoanListlAPIView.as_view(), name="list_loans"),
    path(
        "detail/<str:external_id>/",
        LoanDetailAPIView.as_view(),
        name="detail_loan",
    ),
]
