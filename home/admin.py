from django.contrib import admin
# from django.contrib.auth.models import User
from .models import *


admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Product)
admin.site.register(Player)
admin.site.register(Fixture)
admin.site.register(Team)
admin.site.register(Partner)
admin.site.register(Tag)
admin.site.register(FixtureResult)
