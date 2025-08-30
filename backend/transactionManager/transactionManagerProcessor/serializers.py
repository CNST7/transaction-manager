from rest_framework import serializers

from transactionManagerProcessor.models import CSVProcessingStatus, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def validate_quantity(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Quantity must be integer type")
        return value


class CSVProcessingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVProcessingStatus
        fields = ["status", "no_fails", "no_successes"]


class QueryParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False, allow_null=True)
    date_to = serializers.DateField(required=False, allow_null=True)

    def validate(self, data):
        if (
            data["date_from"]
            and data["date_to"]
            and data["date_from"] > data["date_to"]
        ):
            raise serializers.ValidationError(
                "`date_from` cannot occur after `date_to`"
            )
        return data


class IDSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
