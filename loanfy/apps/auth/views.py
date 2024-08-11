from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        tags=["Auth"],
        methods=["POST"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):

    @extend_schema(
        tags=["Auth"],
        methods=["POST"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
