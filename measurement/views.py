from rest_framework import viewsets 
from rest_framework.response import Response
from .models import Sensor, Measurement
from .serializers import SensorSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def update(self, request, pk):
        sensor = self.get_object()
        serializer = self.get_serializer(sensor, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=HTTP_200_OK)

    def destroy(self, request, pk):
        sensor = self.get_object()
        self.perform_destroy(sensor)
        return Response(status=HTTP_204_NO_CONTENT)