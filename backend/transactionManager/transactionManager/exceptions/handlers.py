import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback

from . import domain_errors

logger = logging.getLogger(__name__)


def global_exception_handler(exc, context: dict) -> Response:
    if response := exception_handler(exc, context):
        return response

    if response := domain_exception_handler(exc, context):
        return response

    logger.exception("UNHANDLED EXCEPTION")
    set_rollback()
    return Response(
        {"detail": str(exc)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def domain_exception_handler(
    exc,
    context: dict,  # noqa: ARG001
) -> Response | None:
    if not isinstance(exc, domain_errors.TransactionManagerBaseError):
        return

    logger.exception("UNHANDLED DOMAIN EXCEPTION")
    set_rollback()
    return Response(
        {"error": str(exc)},
        status=status.HTTP_400_BAD_REQUEST,
    )
