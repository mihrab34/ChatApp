from django.contrib import admin

from .models import Category, Channels, Server

admin.site.register(Category)
admin.site.register(Server)
admin.site.register(Channels)
