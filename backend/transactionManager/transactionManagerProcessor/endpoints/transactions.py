import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from transactionManagerProcessor.serializers import (
    CSVProcessingStatusSerializer,
    TransactionSerializer,
)
from transactionManagerProcessor.models import (
    CSVProcessingStatus,
    Transaction,
    TransactionCSV,
)
from rest_framework import viewsets, mixins
from transactionManagerProcessor.tasks import process_transaction_csv

logger = logging.getLogger(__name__)


class TransactionUploadEndpoint(APIView):
    """Upload transaction CVS file"""

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request: Request):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response(
                {"error": "Missing transactions file"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not csv_file.name.endswith(".csv"):
            return Response(
                {"error": "Not a CSV type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction_csv = TransactionCSV.objects.create(file=csv_file)
        process_transaction_csv.delay(transaction_csv.id)

        return Response(
            {"transaction_csv_id": transaction_csv.id},
            status=status.HTTP_200_OK,
        )


class TransactionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["customer_id", "product_id"]


class ProcessingStatusEndpoint(APIView):
    def get(self, request: Request, transaction_csv_id=None):
        processing_status = CSVProcessingStatus.objects.get(
            transaction_csv=transaction_csv_id
        )
        serializer = CSVProcessingStatusSerializer(processing_status)
        return Response(serializer.data)
