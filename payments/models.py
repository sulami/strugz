from django.db import models

from users.models import User

class Payment(models.Model):
    amount = models.IntegerField()
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User)

