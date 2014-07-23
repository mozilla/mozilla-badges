from django.contrib import admin
from models import Team


class TeamAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Team, TeamAdmin)
