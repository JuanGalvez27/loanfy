from apps.customers.models import Customer
from apps.customers.serializers import (
    CustomerBalanceSerializer,
    CustomerSerializer,
    CustomerWriteSerializer,
)
from apps.loans.models import Loan
from apps.responses import (
    HTTP_response_400,
    HTTP_response_401,
    HTTP_response_404,
    HTTP_response_500,
)
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Customer"],
        methods=["POST"],
        summary="Create a Customer",
        request=CustomerWriteSerializer,
        responses={
            201: OpenApiResponse(
                response=CustomerSerializer,
                description="Created",
            ),
            400: HTTP_response_400,
            401: HTTP_response_401,
            500: HTTP_response_500,
        },
    )
    def post(self, request, *args, **kwargs):
        """Create Customer

        Args:

            external_id: Customer external id
            score: Score of the customer

        Example:

            {
                "external_id": "external_01",
                "score": 700
            }

        Returns:

            JSON with data of the created customer.

        """
        data = request.data
        serializer = CustomerWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        customer_serializer = CustomerSerializer(data=serializer.data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Customer"],
        methods=["GET"],
        summary="List of Customers",
        responses={
            200: OpenApiResponse(
                response=CustomerSerializer,
                description="Created",
            ),
            401: HTTP_response_401,
            500: HTTP_response_500,
        },
    )
    def get(self, request, *args, **kwargs):
        """Create Customer

        Returns:

            JSON with the list of customers.

        """
        customers = Customer.objects.all()
        customer_serializer = CustomerSerializer(customers, many=True)
        return Response(customer_serializer.data, status=status.HTTP_200_OK)


class CustomerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Customer"],
        methods=["GET"],
        summary="Get Customer info",
        responses={
            200: OpenApiResponse(
                response=CustomerSerializer,
                description="OK",
            ),
            404: HTTP_response_404,
            401: HTTP_response_401,
            500: HTTP_response_500,
        },
    )
    def get(self, request, external_id):
        """
        Customer Detail

        Args:

            external_id: Customer external id

        Returns:

            JSON with de data of the customer.
        """
        try:
            customer = Customer.objects.get(external_id=external_id)
        except Customer.DoesNotExist:
            return Response(
                {"message": "No customer found"}, status=status.HTTP_404_NOT_FOUND
            )
        customer_serializer = CustomerSerializer(customer)
        return Response(customer_serializer.data, status=status.HTTP_200_OK)


class CustomerBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Customer"],
        methods=["GET"],
        summary="Get Customer Balance",
        responses={
            200: OpenApiResponse(
                response=CustomerSerializer,
                description="OK",
            ),
            404: HTTP_response_404,
            401: HTTP_response_401,
            500: HTTP_response_500,
        },
    )
    def get(self, request, external_id):
        """
        Customer Balance

            external_id: Customer external id

        Returns:

            JSON with de data of the balance.
        """
        try:
            customer = Customer.objects.get(external_id=external_id)
        except Customer.DoesNotExist:
            return Response(
                {"message": "No customer found"}, status=status.HTTP_404_NOT_FOUND
            )
        loan = Loan()
        total_outstanding = loan.get_customer_balance(customer)
        customer_balance = {
            "external_id": customer.external_id,
            "score": customer.score,
            "total_debt": total_outstanding,
            "available_amount": (customer.score - total_outstanding),
        }
        customer_serializer = CustomerBalanceSerializer(customer_balance)
        return Response(customer_serializer.data, status=status.HTTP_200_OK)
