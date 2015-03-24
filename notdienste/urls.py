from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('registration.backends.default.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html',
        'redirect_field_name': 'redirect'},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),
    url(r'^p/', include('payments.urls', namespace='payments')),
    url(r'', include('services.urls', namespace='services')),
)

