from typing import Any
from uuid import UUID

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.urls import reverse
from rest_framework import status
from transactionManagerProcessor.enums import ProcessingStatus
from transactionManagerProcessor.models import Transaction, TransactionCSV

pytestmark = pytest.mark.django_db(transaction=True)


class TestTransations_Upload:
    def test_transations_upload(
        self,
        client: Client,
        csv_file: SimpleUploadedFile,
    ):
        url = reverse("transactionUpload")
        response = client.post(
            url,
            {"file": csv_file},
            format="multipart",
            headers={
                "content_disposition": "attachment; filename={filename}",
            },
        )
        content: dict[str, Any] = response.json()
        csv_file_upload_id = content.get("transaction_csv_id")
        assert response.status_code == 200
        csv_file_saved = TransactionCSV.objects.get(id=csv_file_upload_id)
        assert csv_file_upload_id
        assert csv_file_saved

    def test_transations_upload_ignores_excessive_fields_in_csv_file(
        self,
        client: Client,
        excessive_fields_csv_file: SimpleUploadedFile,
    ):
        url = reverse("transactionUpload")
        response = client.post(
            url,
            {"file": excessive_fields_csv_file},
            format="multipart",
            headers={
                "content_disposition": "attachment; filename={filename}",
            },
        )
        content: dict[str, Any] = response.json()
        csv_file_upload_id = content.get("transaction_csv_id")
        assert response.status_code == 200
        csv_file_saved = TransactionCSV.objects.get(id=csv_file_upload_id)
        assert csv_file_upload_id
        assert csv_file_saved

    def test_transations_upload_corrupted_csv_file(
        self,
        client: Client,
        corrupted_csv_file: SimpleUploadedFile,
    ):
        url = reverse("transactionUpload")
        response = client.post(
            url,
            {"file": corrupted_csv_file},
            format="multipart",
            headers={
                "content_disposition": "attachment; filename={filename}",
            },
        )
        assert response.status_code == 400
        content: dict[str, Any] = response.json()
        error_message = content.get("error")
        assert error_message == "Invalid CSV format"

    def test_transations_upload_missing_headers_csv_file(
        self,
        client: Client,
        missing_headers_csv_file: SimpleUploadedFile,
    ):
        url = reverse("transactionUpload")
        response = client.post(
            url,
            {"file": missing_headers_csv_file},
            format="multipart",
            headers={
                "content_disposition": "attachment; filename={filename}",
            },
        )
        assert response.status_code == 400
        content: dict[str, Any] = response.json()
        error_message = content.get("error")
        assert "Missing csv headers" in error_message
        assert "transaction_id" in error_message
        assert "currency" in error_message

    def test_transations_upload_empty_csv_file(
        self,
        client: Client,
        empty_csv_file: SimpleUploadedFile,
    ):
        url = reverse("transactionUpload")
        response = client.post(
            url,
            {"file": empty_csv_file},
            format="multipart",
            headers={
                "content_disposition": "attachment; filename={filename}",
            },
        )
        assert response.status_code == 400
        content: dict[str, Any] = response.json()
        error_message = content.get("error")
        assert error_message == "Empty csv file"

    def test_transations_upload_missing_file(
        self,
        client: Client,
    ):
        url = reverse("transactionUpload")
        response = client.post(
            url,
            {"file": ""},
            format="multipart",
            headers={
                "content_disposition": "attachment; filename={filename}",
            },
        )
        assert response.status_code == 400
        content: dict[str, Any] = response.json()
        error_message = content.get("error")
        assert error_message == "Missing transaction file"

    def test_transations_upload_not_a_csv_file(
        self,
        client: Client,
        txt_file: SimpleUploadedFile,
    ):
        url = reverse("transactionUpload")
        response = client.post(
            url,
            {"file": txt_file},
            format="multipart",
            headers={
                "content_disposition": "attachment; filename={filename}",
            },
        )
        assert response.status_code == 400
        content: dict[str, Any] = response.json()
        error_message = content.get("error")
        assert error_message == "Not a CSV type"


class TestTransations_List:
    def test_transactions_list(
        self,
        client: Client,
        create_1000_transactions,
    ):
        url = reverse("transaction-list")
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK

        transaction_fields = (
            "transaction_id",
            "timestamp",
            "amount",
            "currency",
            "customer_id",
            "product_id",
            "quantity",
        )
        assert all(
            field in response.json().get("results")[0] for field in transaction_fields
        )

        pagination_fields = "next", "previous", "results", "count"
        assert all(field in response.json() for field in pagination_fields)

        assert response.json().get("count") == 1000
        assert len(response.json().get("results")) == 100

    def test_transactions_list_filters_product_id(
        self,
        client: Client,
        create_1000_transactions,
        product_id_a: UUID,
    ):
        url = reverse("transaction-list")

        response = client.get(
            url,
            format="json",
            content_type="application/json",
            query_string={"product_id": str(product_id_a)},
        )

        assert response.status_code == status.HTTP_200_OK

        content: dict[str, Any] = response.json()
        transactions: list[dict[str, Any]] = content.get("results")
        unique_products = {
            transaction.get("product_id") for transaction in transactions
        }
        assert unique_products == {str(product_id_a)}

    def test_transactions_list_filters_customer_id(
        self,
        client: Client,
        create_1000_transactions,
        customer_id_a: UUID,
    ):
        url = reverse("transaction-list")

        response = client.get(
            url,
            format="json",
            content_type="application/json",
            query_string={"customer_id": str(customer_id_a)},
        )

        assert response.status_code == status.HTTP_200_OK

        unique_customers = {
            transaction.get("customer_id")
            for transaction in response.data.get("results")
        }
        assert unique_customers == {str(customer_id_a)}


class TestTransations_Retrieve:
    def test_transations_details(
        self,
        client: Client,
    ):
        transaction_data = {
            "transaction_id": "d2993a99-3358-41af-8047-070fa648d079",
            "timestamp": "2025-07-02T20:48:45.336874",
            "amount": "10.00",
            "currency": "PLN",
            "customer_id": "51f53702-b492-47be-b20d-80b6852368dd",
            "product_id": "985e4402-5d1e-404b-8254-968070a3c7c7",
            "quantity": 10,
        }
        Transaction.objects.create(**transaction_data)

        url = reverse("transaction-detail", args=[transaction_data["transaction_id"]])
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK
        expected_data = {
            **transaction_data,
            "timestamp": "2025-07-02T20:48:45.336874Z",
        }
        assert response.json() == expected_data


class TestTransations_ProcessingStatus:
    def test_transations_processing_status(
        self,
        client: Client,
        csv_file: SimpleUploadedFile,
    ):
        url = reverse("transactionUpload")
        response = client.post(
            url,
            {"file": csv_file},
            format="multipart",
            headers={
                "content_disposition": "attachment; filename={filename}",
            },
        )

        content: dict[str, Any] = response.json()
        transaction_csv_id = content.get("transaction_csv_id")
        assert transaction_csv_id
        url = reverse(
            "processingStatus",
            kwargs={"transaction_csv_id": str(transaction_csv_id)},
        )
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert content == {
            "status": ProcessingStatus.PROCESSING,
            "no_fails": 0,
            "no_successes": 0,
        }
