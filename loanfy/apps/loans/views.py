from apps.loans.models import Loan
from apps.loans.serializers import LoanSerializer
from apps.responses import (
    HTTP_response_400,
    HTTP_response_401,
    HTTP_response_404,
    HTTP_response_500,
)
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LoanCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Loan"],
        methods=["POST"],
        summary="Create a Loan",
        request=LoanSerializer,
        responses={
            201: OpenApiResponse(
                response=LoanSerializer,
                description="Created",
            ),
            400: HTTP_response_400,
            401: HTTP_response_401,
            500: HTTP_response_500,
        },
    )
    def post(self, request, *args, **kwargs):
        """Create Loan

        Args:
            customer: UUID, UUID of the costumer
            external_id: str,  Loan external id
            amount: Decimal, Amount of the loan
            status: int, Status of the loan
            contract_version: str, Extra information about the loan
            maximum_payment_date: str: Max pyment day of the loan.

        Example:

            {
                "customer": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "external_id": "string",
                "amount": "-91861350",
                "status": 1,
                "contract_version": "string",
                "maximum_payment_date": "2024-08-13T01:17:54.955Z"
            }

        Returns:

            JSON with data of the created customer.

        """
        data = request.data
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanDetailAPIView(APIView):
    """Detail Loan

    Returns:

        JSON with data of the data of loan.

    """

    permission_classes = [IsAuthenticated]

    def get_object(self, external_id):
        try:
            return Loan.objects.get(external_id=external_id)
        except Loan.DoesNotExist:
            return Response(
                {"message": "No loan found"}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        tags=["Loan"],
        methods=["GET"],
        summary="Get Loan detail",
        responses={
            200: OpenApiResponse(
                response=LoanSerializer,
                description="OK",
            ),
            404: HTTP_response_404,
            401: HTTP_response_401,
            500: HTTP_response_500,
        },
    )
    def get(self, request, external_id, *args, **kwargs):
        """Detail Loan

        Args:

            external_id: Loan external id

        Returns:

            JSON with de data of the loan.

        """
        loan = self.get_object(external_id)
        loan_serializer = LoanSerializer(loan)
        return Response(loan_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Loan"],
        methods=["PATCH"],
        summary="Update Loan data",
        request=LoanSerializer,
        responses={
            200: OpenApiResponse(
                response=LoanSerializer,
                description="OK",
            ),
            400: HTTP_response_400,
            404: HTTP_response_404,
            401: HTTP_response_401,
            500: HTTP_response_500,
        },
    )
    def patch(self, request, external_id):
        data = request.data
        loan = self.get_object(external_id)
        serializer = LoanSerializer(loan, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Loan"],
        methods=["GET"],
        summary="Get Loan list",
        request=LoanSerializer,
        parameters=[
            OpenApiParameter(
                name="customer_external_id",
                location=OpenApiParameter.QUERY,
                description="Customer External ID",
                required=False,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=LoanSerializer,
                description="OK",
            ),
            401: HTTP_response_401,
            500: HTTP_response_500,
        },
    )
    def get(self, request, *args, **kwargs):
        """List Loans with Customer Extenal ID filter

        Returns:

            JSON with de list of the loans.

        """
        customer_external_id = request.query_params.get("customer_external_id", None)
        query = {}
        if customer_external_id:
            query["customer__external_id"] = customer_external_id
        loans = Loan.objects.filter(**query)
        loans_serializer = LoanSerializer(loans, many=True)
        return Response(loans_serializer.data, status=status.HTTP_200_OK)
