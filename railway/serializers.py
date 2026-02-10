from rest_framework import serializers

from railway.models import Station, Route, TrainType, Train, Crew, Journey


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


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type"
        )


class TrainListSerializer(TrainSerializer):
    train_type = serializers.CharField(source="train_type.name")

    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type"
        )


class TrainDetailSerializer(TrainSerializer):
    train_type = TrainTypeSerializer()

    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type"
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "crew",
            "departure_time",
            "arrival_time"
        )


class JourneyListSerializer(JourneySerializer):
    route_name = serializers.CharField(source="route.route_name")
    train_name = serializers.CharField(source="train.name")

    class Meta:
        model = Journey
        fields = (
            "id",
            "route_name",
            "train_name",
            "departure_time",
            "arrival_time"
        )


class JourneyDetailSerializer(JourneySerializer):
    route = RouteDetailSerializer()
    train = TrainDetailSerializer()
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "crew",
            "departure_time",
            "arrival_time"
        )