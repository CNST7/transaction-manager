import csv
import io
import logging

from django.core.files.uploadedfile import UploadedFile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transactionManagerProcessor.models import (
    CSVProcessingStatus,
    Transaction,
    TransactionCSV,
)
from transactionManagerProcessor.serializers import (
    CSVProcessingStatusSerializer,
    TransactionSerializer,
)
from transactionManagerProcessor.tasks import process_transaction_csv

logger = logging.getLogger(__name__)


class TransactionUploadEndpoint(APIView):
    """Upload transaction CVS file"""

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request: Request):
        file: UploadedFile = request.FILES.get("file")
        if error_response := _validate_file(file):
            return error_response

        transaction_csv = TransactionCSV.objects.create(file=file)
        process_transaction_csv.delay(transaction_csv.id)

        return Response(
            {"transaction_csv_id": transaction_csv.id},
            status=status.HTTP_200_OK,
        )


def _validate_file(file: UploadedFile) -> None | Response:
    if not file:
        return Response(
            {"error": "Missing transaction file"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not file.name.endswith(".csv"):
        return Response(
            {"error": "Not a CSV type"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if file.size == 0:
        return Response(
            {"error": "Empty csv file"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        decoded_file = file.read().decode("utf-8")
    except UnicodeDecodeError:
        return Response(
            {"error": "Invalid CSV format"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    reader = csv.DictReader(io.StringIO(decoded_file))
    csv_headers = set(reader.fieldnames)

    required_csv_headers = {
        "transaction_id",
        "timestamp",
        "amount",
        "currency",
        "customer_id",
        "product_id",
        "quantity",
    }

    if csv_headers < required_csv_headers:
        missing_csv_headers = ", ".join(required_csv_headers - csv_headers)
        return Response(
            {"error": f"Missing csv headers: {missing_csv_headers}"},
            status=status.HTTP_400_BAD_REQUEST,
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
