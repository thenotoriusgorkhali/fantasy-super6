from django.contrib import admin
from .models import PlayerPerformance

@admin.register(PlayerPerformance)
class PlayerPerformanceAdmin(admin.ModelAdmin):
    list_display = ['player', 'tournament', 'runs_scored', 'wickets_taken', 'catches', 'fantasy_points']
    list_editable = ['runs_scored', 'wickets_taken', 'catches']
    list_filter = ['tournament']
    search_fields = ['player__name']
    readonly_fields = ['base_points', 'fantasy_points']
    
    fieldsets = (
        ('Basic Info', {'fields': ('player', 'tournament', 'notes')}),
        ('Batting', {'fields': ('runs_scored', 'balls_faced', 'fours', 'sixes', 'is_out')}),
        ('Bowling', {'fields': ('overs_bowled', 'wickets_taken', 'runs_conceded', 'maidens')}),
        ('Fielding', {'fields': ('catches', 'run_outs', 'stumpings')}),
        ('Points (Auto-calculated)', {'fields': ('base_points', 'fantasy_points')}),
    )
