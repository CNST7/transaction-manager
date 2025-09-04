import csv
import io
import logging

from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def validate_csv_file(file: UploadedFile) -> None | Response:
    if not file:
        error_message = "Missing transaction file"
        return _prepare_validation_error_response(error_message)

    if not file.name.endswith(".csv"):
        error_message = "Not a CSV type"
        return _prepare_validation_error_response(error_message)

    if file.size == 0:
        error_message = "Empty csv file"
        return _prepare_validation_error_response(error_message)

    try:
        decoded_file = file.read().decode("utf-8")
    except UnicodeDecodeError:
        error_message = "Invalid CSV format"
        return _prepare_validation_error_response(error_message)

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
        error_message = f"Missing csv headers: {missing_csv_headers}"
        return _prepare_validation_error_response(error_message)


def _prepare_validation_error_response(error_message) -> Response:
    logger.error(f"FILE VALIDATION ERROR: {error_message}")
    return Response(
        {"error": error_message},
        status=status.HTTP_400_BAD_REQUEST,
    )
