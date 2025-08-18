from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckEndpoint(APIView):
    def get(self, request: Request):
        return Response(True)
