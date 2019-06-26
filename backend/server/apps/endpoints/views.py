import json

from rest_framework import viewsets
from rest_framework import mixins

from apps.endpoints.models import Endpoint
from apps.endpoints.serializers import EndpointSerializer

from apps.endpoints.models import MLAlgorithm
from apps.endpoints.serializers import MLAlgorithmSerializer

from apps.endpoints.models import MLRequest
from apps.endpoints.serializers import MLRequestSerializer

from rest_framework import views, status
from rest_framework.response import Response
from apps.ml.registry import MLRegistry
from server.wsgi import registry

class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class MLAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()


class MLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()

class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):
        
        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version", "0.0.0")
        
        key = MLRegistry.get_key(endpoint_name, algorithm_status, algorithm_version)
        if key not in registry.endpoints:
            return Response(
                {"status": "Error", "message": "ML algorithm not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        algorithm_object = registry.endpoints[key]["algorithm_object"]
        database_object = registry.endpoints[key]["database_object"]

        prediction = algorithm_object.compute_prediction(request.data)

        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            response=prediction,
            feedback="",
            parent_mlalgorithm=database_object,
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id 

        return Response(prediction)
