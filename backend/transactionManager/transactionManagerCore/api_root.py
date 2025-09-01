from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    reports_resource_name = "reports"
    transactions_resource_name = "transactions"
    # utils_resource_name = "utils"

    return Response(
        {
            f"{transactions_resource_name}": reverse(
                "transaction-list", request=request, format=format
            ),
            f"{transactions_resource_name}/upload": reverse(
                "transactionUpload", request=request, format=format
            ),
            # f"{transactions_resource_name}/processing-status/<str:transaction_csv_id>": request.build_absolute_uri(
            #     f"{transactions_resource_name}"
            #     + "/processing-status/{transaction_csv_id}"
            # ),
            f"{reports_resource_name}/customer-summary/<str:customer_id>": request.build_absolute_uri(
                f"{reports_resource_name}" + "/customer-summary/{customer_id}"
            ),
            f"{reports_resource_name}/product-summary/<str:product_id>": request.build_absolute_uri(
                f"{reports_resource_name}" + "/product-summary/{product_id}"
            ),
            # f"{utils_resource_name}/health-check": reverse(
            #     "healthCheck", request=request, format=format
            # ),
            # f"{utils_resource_name}/error": reverse(
            #     "error", request=request, format=format
            # ),
        },
    )
