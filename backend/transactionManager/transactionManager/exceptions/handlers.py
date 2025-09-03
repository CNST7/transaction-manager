import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback

logger = logging.getLogger(__name__)


def global_exception_handler(exc, context: dict) -> Response:
    if response := exception_handler(exc, context):
        return response

    logger.error("UNHANDLED EXCEPTION", exc_info=True)
    set_rollback()
    return Response(
        {"detail": str(exc)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
