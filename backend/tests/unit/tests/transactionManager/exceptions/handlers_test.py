import logging

from pytest import LogCaptureFixture
from pytest_mock import MockerFixture
from transactionManager.exceptions import domain_errors
from transactionManager.exceptions.handlers import (
    domain_exception_handler,
    global_exception_handler,
)


class TestGlobalExceptionHandler:
    def test_global_exception_handler_returns_status_code_500(self):
        mock_exc = Exception()
        mock_context = {}
        resp = global_exception_handler(mock_exc, mock_context)

        assert resp.status_code == 500

    def test_global_exception_handler_returns_exc_message_in_json_detail(self):
        mock_exc = Exception("exc message")
        mock_context = {}
        resp = global_exception_handler(mock_exc, mock_context)

        assert resp.data == {"detail": "exc message"}

    def test_global_exception_handler_creates_error_log(
        self,
        caplog: LogCaptureFixture,
    ):
        logger = logging.getLogger("transactionManager")
        logger.propagate = True
        caplog.set_level(logging.ERROR, "transactionManager")

        mock_exc = Exception()
        mock_context = {}
        with caplog.at_level(logging.ERROR):
            global_exception_handler(mock_exc, mock_context)
        assert "ERROR" in caplog.text
        assert "UNHANDLED EXCEPTION" in caplog.text

    def test_global_exception_handler_runs_set_rollback_once(
        self, mocker: MockerFixture
    ):
        mock_set_rollback = mocker.patch(
            "transactionManager.exceptions.handlers.set_rollback"
        )
        mock_exc = Exception()
        mock_context = {}
        global_exception_handler(mock_exc, mock_context)

        mock_set_rollback.assert_called_once()


class TestDomainExceptionHandler:
    def test_domain_exception_handler_returns_status_code_400(self):
        mock_exc = domain_errors.TransactionManagerBaseError()
        mock_context = {}
        resp = domain_exception_handler(mock_exc, mock_context)
        assert resp.status_code == 400

    def test_domain_exception_handler_returns_exc_message_in_json_detail(self):
        mock_exc = domain_errors.TransactionManagerBaseError("exc message")
        mock_context = {}
        resp = domain_exception_handler(mock_exc, mock_context)
        assert resp.data == {"error": "exc message"}

    def test_domain_exception_handler_creates_error_log(
        self,
        caplog: LogCaptureFixture,
    ):
        logger = logging.getLogger("transactionManager")
        logger.propagate = True
        caplog.set_level(logging.ERROR, "transactionManager")

        mock_exc = domain_errors.TransactionManagerBaseError()
        mock_context = {}
        with caplog.at_level(logging.ERROR):
            domain_exception_handler(mock_exc, mock_context)
        assert "ERROR" in caplog.text
        assert "UNHANDLED DOMAIN EXCEPTION" in caplog.text

    def test_domain_exception_handler_runs_set_rollback_once(
        self, mocker: MockerFixture
    ):
        mock_set_rollback = mocker.patch(
            "transactionManager.exceptions.handlers.set_rollback"
        )
        mock_exc = domain_errors.TransactionManagerBaseError()
        mock_context = {}
        domain_exception_handler(mock_exc, mock_context)

        mock_set_rollback.assert_called_once()
