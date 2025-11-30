from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Cruise)
admin.site.register(models.InfoRequest)
admin.site.register(models.Purchase)

# REVIEW ADMIN
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "destination", "cruise", "created_at")
    list_filter = ("rating", "destination", "cruise")
    search_fields = ("user__username", "comment")

# DESTINATION ADMIN
@admin.register(models.Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name',)
