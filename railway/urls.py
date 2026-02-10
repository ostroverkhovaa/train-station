from django.urls import path, include
from rest_framework import routers

from railway.views import (
    StationViewSet,
    RouteViewSet,
    JourneyViewSet,
    OrderViewSet,
    CrewViewSet,
    TrainTypeViewSet,
    TrainViewSet,
)


router = routers.DefaultRouter()
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("crews", CrewViewSet)
router.register("journeys", JourneyViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "railway"
