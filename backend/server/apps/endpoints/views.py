import json

from rest_framework import viewsets
from rest_framework import mixins

from apps.endpoints.models import Endpoint
from apps.endpoints.serializers import EndpointSerializer

from apps.endpoints.models import MLAlgorithm
from apps.endpoints.serializers import MLAlgorithmSerializer

from apps.endpoints.models import MLAlgorithmStatus
from apps.endpoints.serializers import MLAlgorithmStatusSerializer

from apps.endpoints.models import MLRequest
from apps.endpoints.serializers import MLRequestSerializer

from apps.endpoints.models import ABTest
from apps.endpoints.serializers import ABTestSerializer

from rest_framework import views, status
from rest_framework.response import Response
from apps.ml.registry import MLRegistry
from server.wsgi import registry
from django.db import transaction

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

class MLAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.all()


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
        
        if algorithm_version is not None:
            statuses = statuses.filter(parent_mlalgorithm__version = algorithm_version)
        
        if len(statuses) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(statuses) != 1:
            return Response(
                {"status": "Error", "message": "ML algorithm selection is ambiguous. Please specify algorithm version."},
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
        
class ABTestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    serializer_class = ABTestSerializer
    queryset = ABTest.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save()
                # update status for first algorithm
                status_1 = MLAlgorithmStatus(status = "ab_testing", 
                                created_by=instance.created_by, 
                                parent_mlalgorithm = instance.parent_mlalgorithm_1, 
                                parent_endpoint=instance.parent_mlalgorithm_1.parent_endpoint)
                status_1.save()
                # update status for second algorithm
                status_2 = MLAlgorithmStatus(status = "ab_testing", 
                                created_by=instance.created_by, 
                                parent_mlalgorithm = instance.parent_mlalgorithm_2, 
                                parent_endpoint=instance.parent_mlalgorithm_2.parent_endpoint)
                status_2.save()
                
        except Exception as e:
            raise APIException(str(e))