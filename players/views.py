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

    best_bowling_str = f"{best_bowling_wkts}/{best_bowling_runs}" if best_bowling_wkts > 0 else "—"
    best_score_str = f"{best_score}{'*' if not best_score_out else ''}" if best_score > 0 else "—"

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
    }
    return render(request, 'players/detail.html', context)