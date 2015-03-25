from django.db import models

from services.models import User

class Payment(models.Model):
    amount = models.IntegerField()
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return 'Payment {}: {}€ on {} by {}'.format(self.pk, self.amount,
            self.date, self.user)

    def pretty(self):
        return 'Zahlung über {}€ am {}'.format(self.amount, self.date)

