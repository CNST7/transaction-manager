from rest_framework import serializers
from transactionManagerProcessor.models import CSVProcessingStatus, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CSVProcessingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVProcessingStatus
        fields = ["status", "no_fails", "no_successes"]
