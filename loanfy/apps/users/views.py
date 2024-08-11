from apps.users.serializers import UserSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["User"],
        methods=["GET"],
        summary="List users",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(
                response=UserSerializer,
                description="Created",
            ),
            # 400: HTTP_response_400,
            # 401: HTTP_response_401,
            # 500: HTTP_response_500,
        },
    )
    def get(self, request, *args, **kwargs):
        """List users

        Returns:
            Retrieves a list of all the users

        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
