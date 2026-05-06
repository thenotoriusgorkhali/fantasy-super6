from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'role', 'price', 'batting_rating', 'bowling_rating', 'is_active']
    list_filter = ['team', 'role', 'playing_style', 'is_active']
    search_fields = ['name']
    list_editable = ['is_active']
