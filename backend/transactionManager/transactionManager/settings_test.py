from .settings import *  # noqa: F403
from .utils import BACKEND_PORT_LOCK, BROKER_PORT_LOCK

SECRET_KEY = (
    "django-insecure-32402#aa#1!du%x62-gs%0s5-$p+6jxl^5-2)_#u-!_p6=a_56"  # nosec B105
)
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # type: ignore # noqa: F405
    },
}

PORT_BROKER = BACKEND_PORT_LOCK.port
PORT_RESULT_BACKEND = BROKER_PORT_LOCK.port

CELERY_BROKER_URL = f"pyamqp://guest@localhost:{PORT_BROKER}//"
CELERY_RESULT_BACKEND = f"redis://localhost:{PORT_RESULT_BACKEND}/0"
