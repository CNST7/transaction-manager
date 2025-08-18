from django.urls import include, path
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
    path(
        f"{transactions_resource_name}/processing-status/<str:transaction_csv_id>",
        endpoints.ProcessingStatusEndpoint.as_view(),
        name="processingStatus",
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
