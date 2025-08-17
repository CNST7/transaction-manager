from rest_framework import serializers
from transactionManagerProcessor.models import CSVProcessingStatus, Transaction
from django.utils.timezone import make_naive
from django.db import models
from datetime import datetime


class _NaiveDateTimeField(serializers.DateTimeField):
    def to_representation(self, value: datetime):
        if value and value.tzinfo:
            value = make_naive(value)
        return super().to_representation(value)

    def to_internal_value(self, value):
        dt = super().to_internal_value(value)
        if dt and dt.tzinfo:
            dt = make_naive(dt)
        return dt


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    serializer_field_mapping = (
        serializers.ModelSerializer.serializer_field_mapping.copy()
    )
    serializer_field_mapping[models.DateTimeField] = _NaiveDateTimeField


class CSVProcessingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVProcessingStatus
        fields = ["status", "no_fails", "no_successes"]


class QueryParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False, allow_null=True)
    date_to = serializers.DateField(required=False, allow_null=True)


class IDSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
