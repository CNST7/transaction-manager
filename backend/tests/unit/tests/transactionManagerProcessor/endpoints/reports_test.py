import pytest
from uuid import UUID
from django.test.client import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db(transaction=True)


class TestReports_ProductSummary:
    def test_product_summary(
        self,
        many_transactions_1k,
        product_id_a: UUID,
        client: Client,
    ):
        url = reverse("productSummary", kwargs={"product_id": str(product_id_a)})
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json() == {
            "total_quantity": 4000,
            "total_amount": "81500.00",
            "unique_customers": 2,
        }


class TestReports_CustomerSummary:
    def test_customer_summary(
        self,
        many_transactions_1k,
        customer_id_a: UUID,
        client: Client,
    ):
        url = reverse("customerSummary", kwargs={"customer_id": str(customer_id_a)})
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json() == {
            "total_amount": "81500.00",
            "unique_products": 2,
            "last_transaction": "2025-07-03T16:27:02.593273",
        }

    def test_customer_summary_date_from(
        self,
        three_transactions,
        customer_id_a: UUID,
        client: Client,
    ):
        url = reverse("customerSummary", kwargs={"customer_id": str(customer_id_a)})
        url = f"{url}?date_from=2025-08-02"
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json() == {
            "total_amount": "126.50",
            "unique_products": 1,
            "last_transaction": "2025-08-02T20:48:45.336874",
        }

    def test_customer_summary_date_to(
        self,
        three_transactions,
        customer_id_a: UUID,
        client: Client,
    ):
        url = reverse("customerSummary", kwargs={"customer_id": str(customer_id_a)})
        url = f"{url}?date_to=2025-07-02"
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json() == {
            "total_amount": "100.00",
            "unique_products": 1,
            "last_transaction": "2025-07-02T20:48:45.336874",
        }

    def test_customer_summary_date_from_and_date_to(
        self,
        three_transactions,
        customer_id_a: UUID,
        client: Client,
    ):
        url = reverse("customerSummary", kwargs={"customer_id": str(customer_id_a)})
        url = f"{url}?date_from=2025-07-24&date_to=2025-07-26"
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json() == {
            "total_amount": "20.50",
            "unique_products": 1,
            "last_transaction": "2025-07-25T20:48:45.336874",
        }

    def test_customer_summary_incorrect_date_from(
        self,
        three_transactions,
        customer_id_a: UUID,
        client: Client,
    ):
        url = reverse("customerSummary", kwargs={"customer_id": str(customer_id_a)})
        url = f"{url}?date_from=20253-08-02"
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "date_from": [
                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
            ]
        }

    def test_customer_summary_incorrect_date_to(
        self,
        three_transactions,
        customer_id_a: UUID,
        client: Client,
    ):
        url = reverse("customerSummary", kwargs={"customer_id": str(customer_id_a)})
        url = f"{url}?date_to=asdf"
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "date_to": [
                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
            ]
        }
