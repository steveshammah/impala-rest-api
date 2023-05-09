from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import *


admin.site.register(FixtureResult)

@admin.register(Fixture)
class FixtureAdmin(OSMGeoAdmin):
    default_lat = -150000
    default_lon = 4100000
    default_zoom = 12
