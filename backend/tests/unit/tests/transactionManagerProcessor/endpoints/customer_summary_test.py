from uuid import UUID

import pytest
from django.test.client import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db(transaction=True)


class TestReports_CustomerSummary:
    def test_customer_summary(
        self,
        customer_summary_transactions,
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
            "total_amount": "930.00",
            "unique_products": 2,
            "last_transaction": "2025-08-03 10:00:00",
        }

    def test_customer_summary_wrong_currency_exchange_strategy(
        self,
        customer_id_a: UUID,
        client: Client,
    ):
        url = reverse("customerSummary", kwargs={"customer_id": str(customer_id_a)})
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
