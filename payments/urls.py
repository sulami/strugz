from django.conf.urls import patterns, include, url
from django.conf import settings

from payments import views

urlpatterns = patterns('payments.views',
    url(r'^p/$', 'payment', name='payment'),
    url(r'^co/$', 'checkout', name='checkout'),
)
