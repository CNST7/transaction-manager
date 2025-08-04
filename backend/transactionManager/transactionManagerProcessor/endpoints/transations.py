import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from transactionManagerProcessor.serializers import TransactionSerializer
from transactionManagerProcessor.models import Transaction, TransactionCSV
from rest_framework import viewsets, mixins
from transactionManagerProcessor.tasks import process_transactions_csv
from celery.result import AsyncResult
from transactionManager.celery import app


logger = logging.getLogger("transactionManagerProcessor")


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

        saved_csv = TransactionCSV.objects.create(file=csv_file)
        result: AsyncResult = process_transactions_csv.delay(saved_csv.id)

        return Response(
            {
                "transaction_csv_id": saved_csv.id,
                "celery_task_id": result.id,
            },
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

    def get(self, request: Request, task_id=None):
        task_result = AsyncResult(task_id, app=app)

        return Response(
            {"task_status": task_result.status},
            status=status.HTTP_200_OK,
        )
