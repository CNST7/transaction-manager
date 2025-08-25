from django.urls import path

from transactionManagerCore import endpoints

utils_resource_name = "utils"

urlpatterns = [
    path(
        f"{utils_resource_name}/health-check",
        endpoints.HealthCheckEndpoint.as_view(),
        name="healthCheck",
    ),
]
