from django.contrib import admin
from web.models import * 

# Register your models here.
admin.site.register(Film)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Language)
admin.site.register(Genre)