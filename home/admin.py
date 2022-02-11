from django.contrib import admin
# from django.contrib.auth.models import User
from .models import *

# Register your models here.
admin.site.register(Articles)
admin.site.register(Author)
admin.site.register(Product)
# admin.site.register(Player)
# admin.site.register(Fixture)
# admin.site.register(Team)
# admin.site.register(Partner)
