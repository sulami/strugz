from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    plz = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.plz) + ' - ' + self.name

class Service(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True)
    tel = models.CharField(max_length=15)
    website = models.URLField(blank=True)
    plz = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()

    def __unicode__(self):
        return self.name

    def average_rating(self):
        try:
            l = []
            for r in Rating.objects.filter(of=self):
                l += [r.stars]
            return round(sum(l)/float(len(l)), 2)
        except:
            return 0

class Rating(models.Model):
    by = models.ForeignKey(settings.AUTH_USER_MODEL)
    of = models.ForeignKey(Service)
    at = models.DateTimeField(auto_now=True)
    stars = models.IntegerField()
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.by.username + '  - ' + self.of.name
