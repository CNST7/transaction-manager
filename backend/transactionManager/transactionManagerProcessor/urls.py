from django.urls import path, include

from rest_framework.routers import DefaultRouter
from transactionManagerProcessor import endpoints

transactions_resource_name = "transactions"
transactions_router = DefaultRouter(trailing_slash=False)
transactions_router.register(
    transactions_resource_name, endpoints.TransactionViewSet, basename="transaction"
)
reports_resource_name = "reports"


urlpatterns = [
    path(
        f"{transactions_resource_name}/upload",
        endpoints.TransactionUploadEndpoint.as_view(),
        name="transactionUpload",
    ),
    path("", include(transactions_router.urls)),
    path(
        f"{reports_resource_name}/customer-summary/<str:customer_id>",
        endpoints.CustomerSummaryEndpoint.as_view(),
        name="customerSummary",
    ),
    path(
        f"{reports_resource_name}/product-summary/<str:product_id>",
        endpoints.ProductSummaryEndpoint.as_view(),
        name="productSummary",
    ),
]
