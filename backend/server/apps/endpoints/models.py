from django.db import models

class Endpoint(models.Model):
    '''
    The Endpoint object represents ML API endpoint.

    Attributes:
        name: The name of the endpoint, it will be used in API URL,
        owner: The string with owner name,
        created_at: The date when endpoint was created.
    '''
    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class MLAlgorithm(models.Model):
    '''
    The MLAlgorithm represent the ML algorithm object.

    Attributes:
        name: The name of the algorithm.
        description: The short description how algorithm works.
        code: The code of the algorithm.
        status: The status of algorithm in the endpoint. Can be: testing, staging, production.
        version: The version of the algorithm similar to software versioning.
        owner: The name of the owner.
        created_at: The data when MLAlgorithm was added.
        parent_endpoint: The reference to the endpoint.
    '''
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    code = models.CharField(max_length=50000)
    status = models.CharField(max_length=128)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)


class MLRequest(models.Model):
    '''
    The MLRequest will keep information about all requests to ML algorithms.

    Attributes:
        input_data: The input data to ML algorithm in JSON format.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_at: The date when request was created.
        parent_mlalgorithm: The reference to MLAlgorithm used to compute response.
    '''
    input_data = models.CharField(max_length=10000) 
    response = models.CharField(max_length=10000) 
    feedback = models.CharField(max_length=10000) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)

class ABTest(models.Model):
    '''
    '''
    title = models.CharField(max_length=10000) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm_1 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)
    parent_mlalgorithm_2 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)