from apps.endpoints.models import Endpoint
from apps.endpoints.models import MLAlgorithm

class MLRegistry:
    def __init__(self):
        self.endpoints = {}

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
        key = endpoint_name + "_" + algorithm_status
        # add to registry
        self.endpoints[key] ={"algorithm_object": algorithm_object,
                              "database_object": database_object }