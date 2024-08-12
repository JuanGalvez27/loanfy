from apps.payments.models import Payment
from apps.payments.serializers import (
    CreatePaymentSerializer,
    PaymentDetailSerializer,
    PaymentListSerializer,
    PaymentSerializer,
)
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class PaymentCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Payment"],
        methods=["POST"],
        summary="Create a Payment",
        request=CreatePaymentSerializer,
        responses={
            201: OpenApiResponse(
                response=PaymentSerializer,
                description="Created",
            ),
            # 400: HTTP_response_400,
            # 401: HTTP_response_401,
            # 500: HTTP_response_500,
        },
    )
    def post(self, request, *args, **kwargs):
        """Create Payment

        Args:

            external_id: External ID of the payment
            total_amount: Amount of the payment
            customer: customer UUID associated to the payment,
            loan: loan UUID associated to the payment

        Example:

            {
                "external_id": "payment_01",
                "total_amount": "100000",
                "customer": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "loan": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }

        Returns:

            JSON with data of the created customer.

        """
        data = request.data
        create_payment_serializer = CreatePaymentSerializer(data=data)
        create_payment_serializer.is_valid(raise_exception=True)
        payment_data = create_payment_serializer.data
        loan = payment_data.pop("loan")
        payment_data["status"] = 1
        payment_serializer = PaymentSerializer(
            data=payment_data, context={"loan": loan}
        )
        if payment_serializer.is_valid():
            payment_serializer.save()
            return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Payment"],
        methods=["GET"],
        summary="Get Payment list",
        parameters=[
            OpenApiParameter(
                name="customer_external_id",
                location=OpenApiParameter.QUERY,
                description="Customer External ID",
                required=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=PaymentListSerializer(many=True),
                description="OK",
            ),
            # 400: HTTP_response_400,
            # 401: HTTP_response_401,
            # 500: HTTP_response_500,
        },
    )
    def get(self, request, *args, **kwargs):
        """List Payment

        Returns:

            JSON with de list of the payments.

        """
        customer_external_id = request.query_params.get("customer_external_id", None)
        payments = Payment.objects.filter(customer__external_id=customer_external_id)
        payments_serializer = PaymentListSerializer(
            payments, many=True, context={"customer_external_id": customer_external_id}
        )
        return Response(payments_serializer.data, status=status.HTTP_200_OK)
