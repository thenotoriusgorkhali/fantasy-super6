from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import PlayerPerformance
from teams.models import FantasyTeam
from tournaments.models import Tournament

def leaderboard(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    teams = FantasyTeam.objects.filter(tournament=tournament).select_related('user').order_by('-total_points')
    
    user_team = None
    if request.user.is_authenticated:
        user_team = teams.filter(user=request.user).first()
    
    performances = PlayerPerformance.objects.filter(tournament=tournament).select_related('player').order_by('-fantasy_points')
    
    top3 = list(teams[:3])
    rest = list(teams[3:])
    
    return render(request, 'scoring/leaderboard.html', {
        'tournament': tournament,
        'top3': top3,
        'rest': rest,
        'teams': teams,
        'user_team': user_team,
        'performances': performances,
        'top_scorer': performances.filter(runs_scored__gt=0).first(),
        'top_bowler': performances.filter(wickets_taken__gt=0).order_by('-wickets_taken').first(),
    })
