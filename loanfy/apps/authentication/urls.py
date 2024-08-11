from apps.authentication.views import CustomTokenObtainPairView, CustomTokenRefreshView
from django.urls import path

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
