from django.contrib import admin
from services.models import Category, Location, Service, Rating

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Service)
admin.site.register(Rating)

