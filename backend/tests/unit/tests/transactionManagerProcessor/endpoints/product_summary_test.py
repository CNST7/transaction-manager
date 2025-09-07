from uuid import UUID

import pytest
from django.test.client import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db(transaction=True)


class TestReports_ProductSummary:
    def test_product_summary(
        self,
        product_summary_transactions,
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
            "total_quantity": 30,
            "total_amount": "930.00",
            "unique_customers": 2,
        }

    def test_product_summary_wrong_currency_exchange_strategy(
        self,
        product_id_a: UUID,
        client: Client,
    ):
        url = reverse("productSummary", kwargs={"product_id": str(product_id_a)})
        url = f"{url}?currency=AAA"
        response = client.get(
            url,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == 400
        error_message: str = response.json().get("error")
        assert error_message.startswith(
            "Currency exchange strategy is not implemented for currency=AAA and fixed_rate=True parameters."
        )
