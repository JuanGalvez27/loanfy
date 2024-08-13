from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from rest_framework import serializers


class ResponseErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(required=False, max_length=255)


HTTP_response_500 = OpenApiResponse(
    response=ResponseErrorSerializer,
    examples=[
        OpenApiExample(
            "Error example",
            value={
                "detail": "An error occurred while processing the service information update request.",
            },
        ),
    ],
    description="Internal Server Error",
)

HTTP_response_400 = OpenApiResponse(
    response=ResponseErrorSerializer,
    examples=[
        OpenApiExample(
            "Error example",
            value={
                "detail": "Error al hacer la solicitud: 400",
            },
        ),
    ],
    description="Bad Request",
)

HTTP_response_401 = OpenApiResponse(
    response=ResponseErrorSerializer,
    examples=[
        OpenApiExample(
            "Error example",
            value={
                "detail": "Usuario no autenticado",
            },
        ),
    ],
    description="Unauthorized",
)

HTTP_response_404 = OpenApiResponse(
    response=ResponseErrorSerializer,
    examples=[
        OpenApiExample(
            "Error example",
            value={
                "detail": "Error 404: not Found",
            },
        ),
    ],
    description="Not Found",
)
