from django.contrib import admin
from .models import PlayerPerformance

@admin.register(PlayerPerformance)
class PlayerPerformanceAdmin(admin.ModelAdmin):
    list_display  = ['player', 'tournament', 'matches_played', 'runs_scored', 'best_score_runs', 'wickets_taken', 'catches', 'missed_catches', 'fantasy_points']
    list_filter   = ['tournament']
    search_fields = ['player__name']
    readonly_fields = ['base_points', 'fantasy_points', 'points_breakdown']

    fieldsets = (
        ('Basic Info', {
            'fields': ('player', 'tournament', 'notes')
        }),
        ('📅 Match Info', {
            'fields': ('matches_played', 'innings_played'),
            'description': 'Total matches/innings played on this tournament day'
        }),
        ('🏏 Batting — Cumulative Totals', {
            'fields': ('runs_scored', 'balls_faced', 'fours', 'sixes', 'ducks'),
            'description': 'Total runs/balls/boundaries across ALL matches on this day'
        }),
        ('🏏 Best Batting Score (Single Innings)', {
            'fields': ('best_score_runs', 'best_score_not_out'),
            'description': 'Highest score in any one innings — used for 50/100 milestone bonus. Check "not out" if player was unbeaten in that innings.'
        }),
        ('🎯 Bowling — Cumulative Totals', {
            'fields': ('overs_bowled', 'wickets_taken', 'runs_conceded', 'maidens'),
            'description': 'Total bowling figures across ALL matches on this day'
        }),
        ('🎯 Best Bowling (Single Match)', {
            'fields': ('best_bowling_wkts', 'best_bowling_runs'),
            'description': 'Best bowling figure in any one match — used for 3-wkt/5-wkt bonus'
        }),
        ('🧤 Fielding', {
            'fields': ('catches', 'stumpings', 'run_outs', 'missed_catches'),
            'description': 'Missed catches deduct 5 pts each'
        }),
        ('⭐ Points (Auto-calculated)', {
            'fields': ('base_points', 'fantasy_points'),
            'description': 'Calculated automatically on save. Player career stats also update automatically.'
        }),
    )