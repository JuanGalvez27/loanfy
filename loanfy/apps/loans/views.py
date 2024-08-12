from apps.loans.models import Loan
from apps.loans.serializers import LoanSerializer
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LoanCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

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
            # 400: HTTP_response_400,
            # 401: HTTP_response_401,
            # 500: HTTP_response_500,
        },
    )
    def post(self, request, *args, **kwargs):
        """Create Loan

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
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

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
            # 400: HTTP_response_400,
            # 401: HTTP_response_401,
            # 500: HTTP_response_500,
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
            # 400: HTTP_response_400,
            # 401: HTTP_response_401,
            # 500: HTTP_response_500,
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


class LoanListlAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Loan"],
        methods=["GET"],
        summary="Get Loan list",
        request=LoanSerializer,
        responses={
            200: OpenApiResponse(
                response=LoanSerializer,
                description="OK",
            ),
            # 400: HTTP_response_400,
            # 401: HTTP_response_401,
            # 500: HTTP_response_500,
        },
    )
    def get(self, request, *args, **kwargs):
        """List Loans

        Returns:

            JSON with de list of the loans.

        """
        loans = Loan.objects.all()
        loans_serializer = LoanSerializer(loans, many=True)
        return Response(loans_serializer.data, status=status.HTTP_200_OK)
