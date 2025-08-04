import socket
from transactionManager.utils import PortLock


def _is_port_in_use(port) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
            return False
        except OSError:
            return True


def test_unlock_port_is_idempotent():
    test_port_lock = PortLock()
    assert True == _is_port_in_use(test_port_lock.port)
    test_port_lock.unlock_port()
    assert False == _is_port_in_use(test_port_lock.port)
    test_port_lock.unlock_port()
    assert False == _is_port_in_use(test_port_lock.port)
