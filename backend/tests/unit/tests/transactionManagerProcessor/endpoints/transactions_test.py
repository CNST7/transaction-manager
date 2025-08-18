from typing import Any
from urllib.parse import urlencode
from uuid import UUID

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.urls import reverse
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

    def test_transations_upload_corrupted_file(self): ...
    def test_transations_upload_missing_file(self): ...
    def test_transations_upload_not_a_csv_file(self): ...


class TestTransations_List:
    def test_transactions_list(
        self,
        client: Client,
        many_transactions_1k,
    ):
        url = reverse("transaction-list")
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200

        transaction_fields = (
            "id",
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
        many_transactions_40,
        product_id_a: UUID,
    ):
        base_url = reverse("transaction-list")
        query_string = urlencode({"product_id": str(product_id_a)})
        url = f"{base_url}?{query_string}"

        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200

        content: dict[str, Any] = response.json()
        transactions: list[dict[str, Any]] = content.get("results")
        unique_products = {
            transaction.get("product_id") for transaction in transactions
        }
        assert unique_products == {str(product_id_a)}

    def test_transactions_list_filters_customer_id(
        self,
        client: Client,
        many_transactions_40,
        customer_id_a: UUID,
    ):
        base_url = reverse("transaction-list")
        query_string = urlencode({"customer_id": str(customer_id_a)})
        url = f"{base_url}?{query_string}"

        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200

        unique_customers = {
            transaction.get("customer_id")
            for transaction in response.data.get("results")
        }
        assert unique_customers == {str(customer_id_a)}


class TestTransations_Retrieve:
    def test_transations_details(
        self,
        single_transaction: Transaction,
        client: Client,
    ):
        url = reverse("transaction-detail", kwargs={"pk": str(single_transaction.id)})
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": "d0466264-1384-4dc0-82d0-39e541b5c121",
            "timestamp": "2025-07-02T20:48:45.336874Z",
            "amount": "25.30",
            "currency": "PLN",
            "customer_id": "a4245004-9354-4b77-8744-19e36372f4cd",
            "product_id": "ae64a915-9711-47f3-a640-be6f517546b1",
            "quantity": 5,
        }


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
        assert response.status_code == 200
        content = response.json()
        assert content == {
            "status": ProcessingStatus.PROCESSING,
            "no_fails": 0,
            "no_successes": 0,
        }
