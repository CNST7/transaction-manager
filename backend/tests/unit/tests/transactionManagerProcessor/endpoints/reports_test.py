import pytest
from uuid import UUID
from django.test.client import Client
from django.urls import reverse
from urllib.parse import urlencode

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
        assert response.data == {
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
        assert response.data == {
            "total_amount": "81500.00",
            "unique_products": 2,
            "last_transaction": "2025-07-03T16:27:02.593273",
        }
