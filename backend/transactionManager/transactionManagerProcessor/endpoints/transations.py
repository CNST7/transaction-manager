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

        # TODO
        # save file
        # pass id to `process_transactions_csv`
        # return ID

        # process csv in celery

        # create view \transactions\file-processing\{file_id} that will return result of file processing

        result: AsyncResult = process_transactions_csv.delay(saved_csv.id)
        # process_transactions_csv.delay(saved_csv.id)
        # process_transactions_csv(saved_csv.id)

        # if csv_file.multiple_chunks():
        #     decoded_file = b"".join(chunk for chunk in csv_file.chunks()).decode(
        #         "utf-8"
        #     )
        # else:
        #     decoded_file = csv_file.read().decode("utf-8")
        # io_string = io.StringIO(decoded_file)
        # reader = csv.DictReader(io_string)

        # for transaction_data in reader:
        #     try:
        #         dto_transaction = TransactionDTO(**transaction_data)
        #         db_transaction = Transaction.from_dto(dto_transaction)
        #         db_transaction.save()
        #         logger.info(f"PROCESSED DATA: {transaction_data}")
        #     except ValidationError as e:
        #         logger.error(f"FAILED DATA: {transaction_data}")
        #     except IntegrityError as e:
        #         logger.error(f"TRANSACTION ALREADY EXIST {db_transaction.id=} ")

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
