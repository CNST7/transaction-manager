from django.test.client import Client
from django.urls import reverse


class TestHealthCheckEndpoint:
    def test_healthcheck_returns_true(self, client: Client):
        response = client.get(reverse("healthCheck"))
        assert response.json() is True

    def test_healthcheck_returns_status_code_200(self, client: Client):
        response = client.get(reverse("healthCheck"))
        assert response.status_code == 200


class TestErrorEndpoint:
    def test_error_returns_error_details(self, client: Client):
        response = client.get(reverse("error"))
        assert response.json() == {"detail": "Boom!"}

    def test_error_returns_status_code_500(self, client: Client):
        response = client.get(reverse("error"))
        assert response.status_code == 500
