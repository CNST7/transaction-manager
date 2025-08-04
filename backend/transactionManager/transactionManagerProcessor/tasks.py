import csv
import io
import logging
from pydantic import ValidationError
from django.db.utils import IntegrityError
from celery import shared_task
from transactionManagerProcessor.models import (
    Transaction,
    TransactionCSV,
    CSVProcessingResult,
)
from transactionManagerProcessor.dto import TransactionDTO

logger = logging.getLogger("transactionManagerProcessor")


@shared_task()
def process_transactions_csv(csv_file_id: str):
    logger.info(f"Starts processing csv {csv_file_id=}.")
    try:
        transction_csv = TransactionCSV.objects.get(id=csv_file_id)
    except TransactionCSV.DoesNotExist():
        logger.error(
            f"Failed to process {csv_file_id}, file does not exist in database."
        )
        return
    csv_file = transction_csv.file
    if csv_file.multiple_chunks():
        decoded_file = b"".join(chunk for chunk in csv_file.chunks()).decode("utf-8")
    else:
        decoded_file = csv_file.read().decode("utf-8")
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)

    fail_counter = 0
    success_counter = 0
    for transaction_data in reader:
        try:
            try:
                dto_transaction = TransactionDTO(**transaction_data)
                db_transaction = Transaction.from_dto(dto_transaction)
                db_transaction.save()
                logger.info(f"PROCESSED DATA: {transaction_data}")
            except Exception as e:
                fail_counter += 1
                raise
        except ValidationError as e:
            logger.error(f"FAILED DATA: {transaction_data}")
        except IntegrityError as e:
            logger.error(f"TRANSACTION ALREADY EXIST {transaction_data}")
        except Exception:
            logger.error(
                f"FAILED TO CREATE TRANSACTION, UNHANDLED ERROR {transaction_data}"
            )
        else:
            success_counter += 1

    res = CSVProcessingResult.objects.create(
        csv_file=transction_csv,
        no_fails=fail_counter,
        no_sucesses=success_counter,
    )
    # res.save()
    logger.info(f"CREATED RESULT ENTITY {res.csv_file.id=}")
