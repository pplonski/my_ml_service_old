from rest_framework import serializers
from apps.endpoints.models import Endpoint
from apps.endpoints.models import MLAlgorithm
from apps.endpoints.models import MLRequest


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "status", "owner", "created_at")
        fields = read_only_fields


class MLAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithm
        read_only_fields = ("id", "name", "status", "owner", "code", "created_at")
        fields = read_only_fields


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = (
            "id",
            "input_data",
            "response",
            "feedback",
            "parent_mlmodel",
        )
        fields = read_only_fields