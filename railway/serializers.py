from rest_framework import serializers

from railway.models import Station, Route, TrainType


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source_name = serializers.CharField(source="source.name")
    destination_name = serializers.CharField(source="destination.name")

    class Meta:
        model = Route
        fields = ("id", "source_name", "destination_name", "distance")


class RouteDetailSerializer(RouteSerializer):
    source = StationSerializer()
    destination = StationSerializer()

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")

