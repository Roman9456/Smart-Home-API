from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='measurements', on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)