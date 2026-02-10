from rest_framework import viewsets

from railway.models import Station
from railway.serializers import StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

