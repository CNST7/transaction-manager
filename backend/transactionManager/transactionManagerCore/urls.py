from django.urls import path

from transactionManagerCore import endpoints

resource_name = "utils"

urlpatterns = [
    path(
        f"{resource_name}/health-check",
        endpoints.HealthCheckEndpoint.as_view(),
        name="healthCheck",
    ),
]
