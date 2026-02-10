from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from railway.models import Station, Route, TrainType
from railway.serializers import StationSerializer, RouteSerializer, RouteListSerializer, RouteDetailSerializer, \
    TrainTypeSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)



