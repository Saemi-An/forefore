from django.contrib import admin

from .models import Cookies, Pickups, Products, Sale, Times

admin.site.register(Sale)
admin.site.register(Products)
admin.site.register(Cookies)
admin.site.register(Times)
admin.site.register(Pickups)
