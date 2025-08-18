from uuid import UUID

import pytest
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
