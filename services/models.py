from django.db import models

class Location(models.Model):
    plz = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.plz) + ' - ' + self.name

class Service(models.Model):
    pass

