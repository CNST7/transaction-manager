import socket
import logging

logger = logging.getLogger("transactionManagerProcessor")


class PortLock:
    def __init__(self, min: int = 32768, max: int = 60999):
        self._min = min
        self._max = max
        assert 32768 <= min <= max <= 65535
        self._socket: socket.socket | None = None
        self._port: int | None = None
        self._lock_port()

    @property
    def port(self):
        return self._port

    def _lock_port(self) -> int:
        s = socket.socket()
        s.bind(("", 0))
        port = s.getsockname()[1]
        while port < self._min or port > self._max:
            s.close()
            s = socket.socket()
            s.bind(("", 0))
            port = s.getsockname()[1]
        self._socket = s
        self._port = port
        logger.debug(f"Locked port {self._port=}, {self._socket=}")

    def unlock_port(self):
        self._socket.close()
        logger.debug(f"Unlocked port {self._port=}, {self._socket=}")

    def __del__(self):
        self.unlock_port()


BACKEND_PORT_LOCK = PortLock()
BROKER_PORT_LOCK = PortLock()
