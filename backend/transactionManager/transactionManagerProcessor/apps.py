from django.apps import AppConfig


class TransactionmanagerprocessorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transactionManagerProcessor"

    def ready(self):
        import transactionManagerProcessor.signals  # noqa: F401
