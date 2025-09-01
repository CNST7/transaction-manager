import logging

from pytest import LogCaptureFixture
from transactionManager.exceptions.handlers import global_exception_handler


class TestCriticalExceptionHandler:
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

    def test_global_exception_handler_creates_critical_log(
        self,
        caplog: LogCaptureFixture,
    ):
        logger = logging.getLogger("transactionManager")
        logger.propagate = True
        caplog.set_level(logging.ERROR, "transactionManager")

        mock_exc = Exception("exc message")
        mock_context = {}
        with caplog.at_level(logging.ERROR):
            global_exception_handler(mock_exc, mock_context)
        assert "ERROR" in caplog.text
        assert "UNHANDLED EXCEPTION" in caplog.text
