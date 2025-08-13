from .settings import *  # noqa: F403

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

CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "rpc://"


CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
