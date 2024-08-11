# from apps.customers.serializers import CustomerWriteSerializer, CustomerSerializer
from apps.customers.models import Customer
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
