from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TransactionCSV, CSVProcessingStatus


@receiver(post_save, sender=TransactionCSV)
def create_CSVProcessingStatus_for_TransactionCSV(sender, instance, created, **kwargs):
    if created:
        _ = CSVProcessingStatus.objects.create(transaction_csv=instance)
