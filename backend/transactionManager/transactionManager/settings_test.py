from collections.abc import Iterable

from .settings import *  # noqa: F403

SECRET_KEY = "django-insecure-32402#aa#1!du%x62-gs%0s5-$p+6jxl^5-2)_#u-!_p6=a_56"  # nosec B105
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # type: ignore # noqa: F405
    },
}

CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "rpc://"


def _set_log_handlers_to_console_only(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "handlers":
                if isinstance(value, dict):
                    continue
                data[key] = ["console"]
            else:
                _set_log_handlers_to_console_only(value)
    elif isinstance(data, Iterable) and not isinstance(data, str):
        for item in data:
            _set_log_handlers_to_console_only(item)


_set_log_handlers_to_console_only(LOGGING)  # type: ignore # noqa: F405
