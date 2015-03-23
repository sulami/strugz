from django.db import models

from services.models import User

class Payment(models.Model):
    amount = models.IntegerField()
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User)

