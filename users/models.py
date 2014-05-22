from django.db import models
from django.contrib.auth.models import AbstractUser
from services.models import Service

class User(AbstractUser):
    provider = models.BooleanField(default=False)
    favourites = models.ManyToManyField(Service, related_name='favourites')

