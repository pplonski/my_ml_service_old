import json

from rest_framework import viewsets
from rest_framework import mixins

from apps.endpoints.models import Endpoint
from apps.endpoints.serializers import EndpointSerializer

from apps.endpoints.models import MLAlgorithm
from apps.endpoints.serializers import MLAlgorithmSerializer

from apps.endpoints.models import MLAlgorithmStatus

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
        algorithm_version = self.request.query_params.get("version")
        
        statuses = MLAlgorithmStatus.objects.filter(parent_endpoint__name = endpoint_name, status = algorithm_status)
        print("objs", statuses)
        
        if len(statuses) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        algorithm_object = registry.endpoints[statuses[0].parent_mlalgorithm.id]
        prediction = algorithm_object.compute_prediction(request.data)

        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            response=prediction,
            feedback="",
            parent_mlalgorithm=statuses[0].parent_mlalgorithm,
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id 

        return Response(prediction)
        