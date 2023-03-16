import imp
from django.contrib import admin
from restaurant.models import Restaurant, TOP_10_RES

@admin.register(Restaurant) 
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address',)

@admin.register(TOP_10_RES) 
class TOP_10_RESAdmin(admin.ModelAdmin):
    list_display = ('current', 'list',)
