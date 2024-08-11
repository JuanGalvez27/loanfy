from django.urls import path
from apps.users.views import (
    UserAPIView
)

urlpatterns = [
    path("list/", UserAPIView.as_view(), name="list_users"),
]
