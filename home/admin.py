from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *


admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Product)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Partner)
admin.site.register(Tag)
admin.site.register(FixtureResult)


@admin.register(Fixture)
class FixtureAdmin(OSMGeoAdmin):
    default_lat = -150000
    default_lon = 4100000
    default_zoom = 12
