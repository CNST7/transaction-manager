from uuid import UUID
import pytest
from django.test.client import Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from urllib.parse import urlencode

from transactionManagerProcessor.models import Transaction


pytestmark = pytest.mark.django_db(transaction=True)


class TestTransations_Upload:
    def test_transations_upload(
        self,
        client: Client,
    ):
        url = reverse("transactionUpload")
        csv_content = b"id,timestamp,amount,currency,customer_id,product_id,quantity\nd0466264-1384-4dc0-82d0-39e541b5c121,2025-07-02 20:48:45.336874,25.30,PLN,14245004-9354-4b77-8744-19e36372f4cd,0e64a915-9711-47f3-a640-be6f517546b1,5"
        filename = "test.csv"

        csv_file = SimpleUploadedFile(
            filename, csv_content, content_type="multipart/form-data"
        )

        response = client.post(
            url,
            {"file": csv_file},
            format="multipart",
            headers={
                f"content_disposition": "attachment; filename={filename}",
            },
        )

        assert response.status_code == 204

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
            (field in response.data.get("results")[0] for field in transaction_fields)
        )

        pagination_fields = "next", "previous", "results", "count"
        assert all((field in response.data for field in pagination_fields))

        assert response.data.get("count") == 1000
        assert len(response.data.get("results")) == 100

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

        unique_products = {
            transaction.get("product_id")
            for transaction in response.data.get("results")
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
        assert response.data == {
            "id": "d0466264-1384-4dc0-82d0-39e541b5c121",
            "timestamp": "2025-07-02T20:48:45.336874Z",
            "amount": "25.30",
            "currency": "PLN",
            "customer_id": "a4245004-9354-4b77-8744-19e36372f4cd",
            "product_id": "ae64a915-9711-47f3-a640-be6f517546b1",
            "quantity": 5,
        }
