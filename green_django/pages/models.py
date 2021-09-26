from django.db import models
from time import time
from django.utils import timezone

from django.db.models.fields import DateTimeField


# Dashoard
class Dashboard(models.Model):
    title = models.CharField(max_length=250, default="")
    icon = models.CharField(max_length=250, default="")
    url = models.CharField(max_length=250, default="")

    def __str__(self):
        return str(self.pk) + ' - ' + self.title

# Device Details
class Detail(models.Model):
    lat = models.CharField(max_length=250, default="")
    lng = models.CharField(max_length=250, default="")
    device_id = models.CharField(max_length=250, default="")
    plant_name = models.CharField(max_length=250, default="")

    def __str__(self):
        r = f'Dev-Id: {self.device_id} - Lat: {self.lat} - Lng: {self.lng} - Plant Name: {self.plant_name}'
        return r

# Soil Temp
class SoilTemp(models.Model):
    soil_temp = models.FloatField(default=0.0)
    date = DateTimeField(default=timezone.now)

    def __str__(self):
        r = f'{self.date} - {self.soil_temp}'
        return r

# Historical Sensor Data
class SensorHisData(models.Model):
    soil_temp = models.FloatField(default=0.0)
    air_temp = models.FloatField(default=0.0)
    soil_moisture = models.FloatField(default=0.0)
    date = DateTimeField(default=timezone.now)
    ts = models.IntegerField(default=0)

    def __str__(self):
        r = f'Date: {self.date} S-temp: {self.soil_temp} - A-temp: {self.air_temp} - S-moisture: {self.soil_moisture}'
        return r