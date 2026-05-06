from django.contrib import admin
from .models import FantasyTeam, FantasyTeamPlayer

class FantasyTeamPlayerInline(admin.TabularInline):
    model = FantasyTeamPlayer
    extra = 0
    readonly_fields = ['points_earned']

@admin.register(FantasyTeam)
class FantasyTeamAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'user', 'tournament', 'total_points', 'rank']
    readonly_fields = ['total_points', 'rank']
    inlines = [FantasyTeamPlayerInline]

@admin.register(FantasyTeamPlayer)
class FantasyTeamPlayerAdmin(admin.ModelAdmin):
    list_display = ['fantasy_team', 'player', 'role_in_team', 'points_earned']
