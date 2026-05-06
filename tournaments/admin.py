from django.contrib import admin
from .models import Tournament

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'match_date', 'deadline', 'is_active', 'is_completed', 'status']
    list_editable = ['is_active', 'is_completed']
    
    def status(self, obj):
        return obj.status()
    status.short_description = 'Status'
