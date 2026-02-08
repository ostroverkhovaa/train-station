from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="source_station"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="destination_station"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"

