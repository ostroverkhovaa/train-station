from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from railway.models import TrainType, Train, Station, Route, Crew, Journey
from railway.serializers import (
    JourneyListSerializer,
    JourneyDetailSerializer
)

JOURNEY_URL = reverse("railway:journey-list")

def sample_journey(**params):
    train_type = TrainType.objects.create(name="Sample train type")
    station_1 = Station.objects.create(name="Sample station 1", longitude=10, latitude=10)
    station_2 = Station.objects.create(name="Sample station 2", longitude=20, latitude=20)
    route = Route.objects.create(
        source=station_1,
        destination=station_2,
        distance=10
    )
    train = Train.objects.create(
        name="Sample train",
        cargo_num=2,
        places_in_cargo=20,
        train_type=train_type
    )
    defaults = {
        "route": route,
        "train": train,
        "departure_time": "2026-01-01T00:00:00Z",
        "arrival_time": "2026-01-02T00:00:00Z"
    }
    defaults.update(params)

    return Journey.objects.create(**defaults)

def detail_url(journey_id):
    return reverse("railway:journey-detail", args=[journey_id])


class UnauthenticatedJourneyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(JOURNEY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedJourneyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_journeys(self):
        sample_journey()
        sample_journey()

        res = self.client.get(JOURNEY_URL)

        journeys = Journey.objects.order_by("id")
        serializer = JourneyListSerializer(journeys, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_journey_detail(self):
        journey = sample_journey()
        journey.crew.add(Crew.objects.create(
            first_name="Sample name",
            last_name="Sample last name")
        )

        url = detail_url(journey.id)
        res = self.client.get(url)

        serializer = JourneyDetailSerializer(journey)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_journey_forbidden(self):
        train_type = TrainType.objects.create(name="Sample train type")
        station_1 = Station.objects.create(name="Sample station 1", longitude=5, latitude=10)
        station_2 = Station.objects.create(name="Sample station 2", longitude=20, latitude=20)
        route = Route.objects.create(
            source=station_1,
            destination=station_2,
            distance=10
        )
        train = Train.objects.create(
            name="Sample train",
            cargo_num=2,
            places_in_cargo=20,
            train_type=train_type
        )
        crew = Crew.objects.create(
            first_name="Sample name",
            last_name="Sample last name"
        )
        payload = {
            "route": route.id,
            "train": train.id,
            "crew": [crew.id],
            "departure_time": "2026-01-01T00:00:00Z",
            "arrival_time": "2026-01-02T00:00:00Z"
        }
        res = self.client.post(JOURNEY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_journeys_by_route(self):
        station_1 = Station.objects.create(
            name="Sample station 1",
            longitude=10,
            latitude=10
        )
        station_2 = Station.objects.create(
            name="Sample station 2",
            longitude=20,
            latitude=20
        )
        route_1 = Route.objects.create(
            source=station_1,
            destination=station_2,
            distance=10
        )
        route_2 = Route.objects.create(
            source=station_2,
            destination=station_1,
            distance=10
        )
        journey_1 = sample_journey(route=route_1)
        journey_2 = sample_journey(route=route_2)
        res = self.client.get(f"{JOURNEY_URL}?route={route_1.id}")

        serializer_1 = JourneyListSerializer(journey_1)
        serializer_2 = JourneyListSerializer(journey_2)

        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)

    def test_filter_journeys_by_date(self):
        journey_1 = sample_journey(departure_time="2026-01-01T00:00:00Z")
        journey_2 = sample_journey(departure_time="2026-01-02T00:00:00Z")
        res = self.client.get(f"{JOURNEY_URL}?date=2026-01-01")

        serializer_1 = JourneyListSerializer(journey_1)
        serializer_2 = JourneyListSerializer(journey_2)

        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)


class AdminJourneyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_journey(self):
        train_type = TrainType.objects.create(name="Sample train type")
        station_1 = Station.objects.create(name="Sample station 1", longitude=5, latitude=10)
        station_2 = Station.objects.create(name="Sample station 2", longitude=20, latitude=20)
        route = Route.objects.create(
            source=station_1,
            destination=station_2,
            distance=10
        )
        train = Train.objects.create(
            name="Sample train",
            cargo_num=2,
            places_in_cargo=20,
            train_type=train_type
        )
        crew = Crew.objects.create(
            first_name="Sample name",
            last_name="Sample last name"
        )
        payload = {
            "route": route.id,
            "train": train.id,
            "crew": [crew.id],
            "departure_time": "2026-01-01T00:00:00Z",
            "arrival_time": "2026-01-02T00:00:00Z"
        }
        res = self.client.post(JOURNEY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        journey = Journey.objects.get(id=res.data["id"])
        self.assertEqual(payload["route"], journey.route.id)
        self.assertEqual(payload["train"], journey.train.id)

        self.assertEqual(
            payload["crew"],
            list(journey.crew.values_list("id", flat=True))
        )

        self.assertEqual(
            payload["departure_time"],
            journey.departure_time.isoformat().replace("+00:00", "Z")
        )
        self.assertEqual(
            payload["arrival_time"],
            journey.arrival_time.isoformat().replace("+00:00", "Z")
        )

    def test_update_journey(self):
        journey = sample_journey()
        payload = {"departure_time": "2026-01-03T00:00:00Z"}
        url = detail_url(journey.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        journey.refresh_from_db()
        self.assertEqual(
            journey.departure_time.isoformat().replace("+00:00", "Z"), payload["departure_time"]
        )

    def test_delete_journey(self):
        journey = sample_journey()
        url = detail_url(journey.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Journey.objects.filter(id=journey.id).exists())
