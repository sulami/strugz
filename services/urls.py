from django.conf.urls import patterns, include, url
from django.conf import settings

from services import views

urlpatterns = patterns('services.views',
    url(r'^$', 'index', name='index'),
    url(r'^e/(\d)/$', 'search', name='search'),
    url(r'^c/(\d)/$', 'category', name='category'),
    url(r'^s/(\d)/$', 'service', name='service'),
    url(r'^m/$', 'manage', name='manage'),
    url(r'^m/v/$', 'verification', name='verification'),
    url(r'^m/pd/$', 'personal_data', name='personal_data'),
)

