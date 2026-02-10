from datetime import datetime
from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from railway.models import Station, Route, TrainType, Train, Crew, Journey, Order
from railway.serializers import (
    StationSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    TrainTypeSerializer,
    TrainListSerializer,
    TrainDetailSerializer,
    TrainSerializer,
    CrewSerializer,
    JourneyListSerializer,
    JourneySerializer,
    JourneyDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
)


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


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.select_related("train_type")
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        if self.action == "retrieve":
            return TrainDetailSerializer
        return TrainSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = (
        Journey.objects.select_related("route", "train")
        .prefetch_related("crew")
        .annotate(
            tickets_available=(
                F("train__cargo_num") * F("train__places_in_cargo")
                - Count("tickets", distinct=True)
            )
        )
    )
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer

    def get_queryset(self):
        queryset = self.queryset
        route_id_str = self.request.query_params.get("route")
        date = self.request.query_params.get("date")

        if route_id_str:
            try:
                queryset = queryset.filter(route_id=int(route_id_str))
            except ValueError:
                pass

        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
                queryset = queryset.filter(departure_time__date=date)
            except ValueError:
                pass

        return queryset


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.prefetch_related(
        "tickets__journey__train",
        "tickets__journey__route"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related(
                "tickets__journey__train",
                "tickets__journey__route"
            )
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
