from django.contrib import admin

from .models import Auction, Category


admin.site.register(Auction)
admin.site.register(Category)
