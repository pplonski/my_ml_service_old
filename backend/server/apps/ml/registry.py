from apps.endpoints.models import Endpoint
from apps.endpoints.models import MLAlgorithm

class MLRegistry:
    def __init__(self):
        self.endpoints = {}

    @staticmethod
    def get_key(endpoint_name, algorithm_status, algorithm_version):
        if algorithm_status == "production":
            return "_".join([endpoint_name, algorithm_status])
        return "_".join([endpoint_name, algorithm_status, algorithm_version])

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name, 
                    algorithm_status, algorithm_version, owner,
                    algorithm_description, algorithm_code):
        # get endpoint
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)
        
        # get algorithm
        database_object, _ = MLAlgorithm.objects.get_or_create(
                name=algorithm_name,
                description=algorithm_description,
                code=algorithm_code,
                status=algorithm_status,
                version=algorithm_version,
                owner=owner,
                parent_endpoint=endpoint)
            
        # specify the key
        key = MLRegistry.get_key(endpoint_name, algorithm_status, algorithm_version)
        # add to registry
        self.endpoints[key] ={"algorithm_object": algorithm_object,
                              "database_object": database_object }