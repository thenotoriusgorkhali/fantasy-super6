from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Tournament
from teams.models import FantasyTeam
from scoring.models import PlayerPerformance

def home(request):
    tournament = Tournament.objects.filter(is_active=True).order_by('-created_at').first()
    user_team = None
    top_teams = []
    if tournament:
        top_teams = FantasyTeam.objects.filter(tournament=tournament).select_related('user').order_by('-total_points')[:3]
        if request.user.is_authenticated:
            user_team = FantasyTeam.objects.filter(user=request.user, tournament=tournament).first()

    from players.models import Player
    player_count = Player.objects.filter(is_active=True).count()
    team_count   = FantasyTeam.objects.count()
    top_score    = FantasyTeam.objects.order_by('-total_points').first()
    # Top players by price for floating cards
    thunder_stars = list(Player.objects.filter(is_active=True, team='Thunder XI').order_by('-price')[:2])
    storm_stars   = list(Player.objects.filter(is_active=True, team='Storm XI').order_by('-price')[:2])

    stats = {
        'players':   player_count,
        'teams':     team_count,
        'top_score': top_score,
    }

    stats_display = [
        ('Active Players', player_count, 'background:linear-gradient(135deg,#00e676,#00bcd4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;', '🏏'),
        ('Teams Created',  team_count,   'background:linear-gradient(135deg,#00bcd4,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;', '👥'),
        ('Max Credits',    60,           'background:linear-gradient(135deg,#ffd700,#ff8f00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;', '💰'),
        ('Players Per Team',6,           'background:linear-gradient(135deg,#a855f7,#6366f1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;', '⚡'),
    ]

    batting_points = [
        {'label':'Per Run',        'pts':'+1'},
        {'label':'Per Four',       'pts':'+1'},
        {'label':'Per Six',        'pts':'+2'},
        {'label':'50+ Bonus',      'pts':'+8'},
        {'label':'100+ Bonus',     'pts':'+16'},
        {'label':'Duck Penalty',   'pts':'-2'},
        {'label':'SR ≥ 170',       'pts':'+6'},
        {'label':'SR < 50',        'pts':'-6'},
    ]
    bowling_points = [
        {'label':'Per Wicket',     'pts':'+25'},
        {'label':'Per Maiden',     'pts':'+8'},
        {'label':'3-Wkt Bonus',    'pts':'+8'},
        {'label':'5-Wkt Bonus',    'pts':'+16'},
        {'label':'Economy ≤ 5',    'pts':'+6'},
        {'label':'Economy ≥ 12',   'pts':'-6'},
    ]

    return render(request, 'tournaments/home.html', {
        'tournament':     tournament,
        'user_team':      user_team,
        'top_teams':      top_teams,
        'stats':          stats,
        'stats_display':  stats_display,
        'batting_points': batting_points,
        'bowling_points': bowling_points,
        'thunder_stars':  thunder_stars,
        'storm_stars':    storm_stars,
    })

def tournament_detail(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    return render(request, 'tournaments/detail.html', {'tournament': tournament})
