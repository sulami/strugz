from django.conf.urls import patterns, include, url
from django.conf import settings

from renderer import views

urlpatterns = patterns('renderer.views',
    url(r'^$', 'index', name='index'),
    url(r'^e/(\d)/$', 'search', name='search'),
    url(r'^c/(\d)/$', 'category', name='category'),
    url(r'^s/(\d)/$', 'service', name='service'),
)
