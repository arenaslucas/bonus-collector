import logging
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import Logger


class TestLogger:
    def test_info_logs_message(self, caplog):
        logger = Logger("test")
        with caplog.at_level(logging.INFO):
            logger.info("test message")
        assert "test message" in caplog.text
        assert "INFO" in caplog.text

    def test_error_logs_message(self, caplog):
        logger = Logger("test")
        with caplog.at_level(logging.ERROR):
            logger.error("error message")
        assert "error message" in caplog.text
        assert "ERROR" in caplog.text

    def test_warning_logs_message(self, caplog):
        logger = Logger("test")
        with caplog.at_level(logging.WARNING):
            logger.warning("warning message")
        assert "warning message" in caplog.text
        assert "WARNING" in caplog.text

    def test_exception_logs_message_with_traceback(self, caplog):
        logger = Logger("test")
        try:
            raise ValueError("test error")
        except ValueError:
            with caplog.at_level(logging.ERROR):
                logger.exception("exception message")
        assert "exception message" in caplog.text
        assert "ValueError" in caplog.text
        assert "test error" in caplog.text
