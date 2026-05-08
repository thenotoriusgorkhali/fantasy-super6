from django.shortcuts import render, get_object_or_404
from .models import Player
from scoring.models import PlayerPerformance

def player_list(request):
    players = Player.objects.filter(is_active=True)
    return render(request, 'players/list.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk, is_active=True)
    performances = PlayerPerformance.objects.filter(player=player).select_related('tournament').order_by('-tournament__match_date')

    # Aggregate career stats from performances
    best_score = 0
    best_score_out = True
    best_bowling_wkts = 0
    best_bowling_runs = 999
    total_runs = 0
    total_balls = 0
    total_wkts = 0
    total_overs = 0
    total_runs_conceded = 0
    total_catches = 0
    total_stumpings = 0
    total_runouts = 0
    total_fours = 0
    total_sixes = 0
    fifties = 0
    hundreds = 0
    total_fantasy_pts = 0
    matches = performances.count()

    for p in performances:
        total_runs += p.runs_scored
        total_balls += p.balls_faced
        total_wkts += p.wickets_taken
        total_overs += p.overs_bowled
        total_runs_conceded += p.runs_conceded
        total_catches += p.catches
        total_stumpings += p.stumpings
        total_runouts += p.run_outs
        total_fours += p.fours
        total_sixes += p.sixes
        total_fantasy_pts += p.fantasy_points
        if p.runs_scored >= 100: hundreds += 1
        if p.runs_scored >= 50: fifties += 1
        # Best score
        if p.runs_scored > best_score:
            best_score = p.runs_scored
            best_score_out = p.is_out
        # Best bowling (most wickets, then fewest runs)
        if p.wickets_taken > best_bowling_wkts or (p.wickets_taken == best_bowling_wkts and p.runs_conceded < best_bowling_runs):
            if p.wickets_taken > 0:
                best_bowling_wkts = p.wickets_taken
                best_bowling_runs = p.runs_conceded

    career_sr = round((total_runs / total_balls * 100), 1) if total_balls > 0 else 0
    career_avg = round(total_runs / matches, 1) if matches > 0 else 0
    career_eco = round(total_runs_conceded / total_overs, 1) if total_overs > 0 else 0
    avg_fantasy = round(total_fantasy_pts / matches, 1) if matches > 0 else 0

    best_score_num = best_score  # numeric version for badge logic
    best_bowling_str = f"{best_bowling_wkts}/{best_bowling_runs}" if best_bowling_wkts > 0 else "—"
    best_score_str = f"{best_score}{'*' if not best_score_out else ''}" if best_score > 0 else "—"

    # Generate dynamic badges based on stats
    badges = []

    # Fantasy performance badges
    if avg_fantasy >= 150:
        badges.append({'icon': '👑', 'text': 'Fantasy King', 'color': '#ffd700', 'bg': 'rgba(255,215,0,0.12)', 'border': 'rgba(255,215,0,0.3)'})
    elif avg_fantasy >= 100:
        badges.append({'icon': '⭐', 'text': 'Fantasy Elite', 'color': '#00e676', 'bg': 'rgba(0,230,118,0.12)', 'border': 'rgba(0,230,118,0.3)'})
    elif avg_fantasy >= 60:
        badges.append({'icon': '🔥', 'text': 'Hot Pick', 'color': '#fb923c', 'bg': 'rgba(249,115,22,0.12)', 'border': 'rgba(249,115,22,0.3)'})

    # Batting badges
    if best_score_num >= 100:
        badges.append({'icon': '💯', 'text': 'Century Maker', 'color': '#fcd34d', 'bg': 'rgba(252,211,77,0.12)', 'border': 'rgba(252,211,77,0.3)'})
    elif best_score_num >= 75:
        badges.append({'icon': '🏏', 'text': 'Big Hitter', 'color': '#60a5fa', 'bg': 'rgba(96,165,250,0.12)', 'border': 'rgba(96,165,250,0.3)'})
    elif best_score_num >= 50:
        badges.append({'icon': '🎯', 'text': 'Consistent Bat', 'color': '#86efac', 'bg': 'rgba(134,239,172,0.12)', 'border': 'rgba(134,239,172,0.3)'})

    # Strike rate badges
    if career_sr >= 160:
        badges.append({'icon': '💥', 'text': 'Power Striker', 'color': '#f87171', 'bg': 'rgba(248,113,113,0.12)', 'border': 'rgba(248,113,113,0.3)'})
    elif career_sr >= 130:
        badges.append({'icon': '⚡', 'text': 'Explosive Batter', 'color': '#fb923c', 'bg': 'rgba(249,115,22,0.12)', 'border': 'rgba(249,115,22,0.3)'})

    # Bowling badges
    if total_wkts >= 5:
        badges.append({'icon': '🎳', 'text': 'Wicket Machine', 'color': '#f87171', 'bg': 'rgba(248,113,113,0.12)', 'border': 'rgba(248,113,113,0.3)'})
    elif total_wkts >= 3:
        badges.append({'icon': '🎯', 'text': 'Key Bowler', 'color': '#fb923c', 'bg': 'rgba(249,115,22,0.12)', 'border': 'rgba(249,115,22,0.3)'})

    # Economy badge
    if career_eco > 0 and career_eco <= 6:
        badges.append({'icon': '🧊', 'text': 'Economy Master', 'color': '#00bcd4', 'bg': 'rgba(0,188,212,0.12)', 'border': 'rgba(0,188,212,0.3)'})

    # Fielding/catches
    if total_catches >= 3:
        badges.append({'icon': '🧤', 'text': 'Safe Hands', 'color': '#c4b5fd', 'bg': 'rgba(196,181,253,0.12)', 'border': 'rgba(196,181,253,0.3)'})

    # Skill rating badges
    if player.batting_rating >= 9:
        badges.append({'icon': '🏆', 'text': 'Elite Batsman', 'color': '#3b82f6', 'bg': 'rgba(59,130,246,0.12)', 'border': 'rgba(59,130,246,0.3)'})
    if player.bowling_rating >= 9:
        badges.append({'icon': '🔴', 'text': 'Elite Bowler', 'color': '#ef4444', 'bg': 'rgba(239,68,68,0.12)', 'border': 'rgba(239,68,68,0.3)'})
    if player.fielding_rating >= 9:
        badges.append({'icon': '💎', 'text': 'Elite Fielder', 'color': '#8b5cf6', 'bg': 'rgba(139,92,246,0.12)', 'border': 'rgba(139,92,246,0.3)'})

    # Role-specific
    role = player.role
    if role == 'AR':
        badges.append({'icon': '⚡', 'text': 'All-Round Threat', 'color': '#a78bfa', 'bg': 'rgba(167,139,250,0.12)', 'border': 'rgba(167,139,250,0.3)'})
    if role == 'WK':
        badges.append({'icon': '🧤', 'text': 'Glove Expert', 'color': '#f97316', 'bg': 'rgba(249,115,22,0.12)', 'border': 'rgba(249,115,22,0.3)'})

    # Milestone badges
    if hundreds >= 1:
        badges.append({'icon': '💯', 'text': f'{hundreds} Centur{"y" if hundreds==1 else "ies"}', 'color': '#ffd700', 'bg': 'rgba(255,215,0,0.12)', 'border': 'rgba(255,215,0,0.3)'})
    if fifties >= 3:
        badges.append({'icon': '🏅', 'text': f'{fifties} Half-Centuries', 'color': '#fcd34d', 'bg': 'rgba(252,211,77,0.12)', 'border': 'rgba(252,211,77,0.3)'})

    # Cap to max 5 most important badges
    badges = badges[:5]

    context = {
        'player': player,
        'performances': performances,
        'matches': matches,
        'best_score': best_score_str,
        'best_bowling': best_bowling_str,
        'career_sr': career_sr,
        'career_avg': career_avg,
        'career_eco': career_eco,
        'total_runs': total_runs,
        'total_wkts': total_wkts,
        'total_catches': total_catches + total_stumpings,
        'total_fours': total_fours,
        'total_sixes': total_sixes,
        'fifties': fifties,
        'hundreds': hundreds,
        'avg_fantasy': avg_fantasy,
        'total_fantasy_pts': round(total_fantasy_pts, 1),
        'badges': badges,
    }
    return render(request, 'players/detail.html', context)
