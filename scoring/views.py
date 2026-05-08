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


def view_team(request, tournament_id, team_id):
    from teams.models import FantasyTeam, FantasyTeamPlayer
    from scoring.models import PlayerPerformance
    from scoring.engine import calculate_points_detailed, apply_multiplier

    tournament = get_object_or_404(Tournament, pk=tournament_id)
    team = get_object_or_404(FantasyTeam, pk=team_id, tournament=tournament)

    performances = {p.player_id: p for p in PlayerPerformance.objects.filter(tournament=tournament)}
    order = {'Captain': 0, 'Vice Captain': 1, 'Player': 2}
    team_players = sorted(team.team_players.select_related('player').all(),
                          key=lambda x: order[x.role_in_team])

    player_data = []
    for tp in team_players:
        perf = performances.get(tp.player_id)
        bd = None
        multiplier = 2.0 if tp.role_in_team == 'Captain' else (1.5 if tp.role_in_team == 'Vice Captain' else 1.0)
        if perf:
            bd = perf.points_breakdown or calculate_points_detailed(perf)
            bd['multiplier'] = multiplier
            bd['final_points'] = round(bd['base_points'] * multiplier, 1)
            bd['sr'] = perf.strike_rate()
            bd['eco'] = perf.economy_rate()

        pts = tp.points_earned
        pts_color = '#ffd700' if pts >= 200 else ('#00e676' if pts >= 100 else ('#00bcd4' if pts >= 40 else '#8899aa'))

        role = tp.player.role
        role_color = {'BAT':'#3b82f6','BOWL':'#ef4444','AR':'#8b5cf6','WK':'#f97316'}.get(role,'#8899aa')
        role_grad  = {'BAT':'linear-gradient(135deg,#3b82f6,#1d4ed8)','BOWL':'linear-gradient(135deg,#ef4444,#991b1b)','AR':'linear-gradient(135deg,#8b5cf6,#6b21a8)','WK':'linear-gradient(135deg,#f97316,#c2410c)'}.get(role,'')
        role_shade = {'BAT':'rgba(59,130,246,0.12)','BOWL':'rgba(239,68,68,0.12)','AR':'rgba(139,92,246,0.12)','WK':'rgba(249,115,22,0.12)'}.get(role,'rgba(255,255,255,0.05)')

        player_data.append({'tp': tp, 'perf': perf, 'bd': bd, 'multiplier': multiplier, 'pts_color': pts_color, 'role_color': role_color, 'role_grad': role_grad, 'role_shade': role_shade})

    # Assign field positions
    bat_pos  = [('12%','25%'),('12%','75%'),('20%','50%'),('20%','15%'),('20%','85%')]
    wk_pos   = [('36%','50%'),('36%','25%'),('36%','75%')]
    ar_pos   = [('52%','20%'),('52%','80%'),('60%','50%'),('44%','50%')]
    bowl_pos = [('74%','28%'),('74%','72%'),('82%','50%'),('68%','50%'),('68%','20%')]
    role_counters = {'BAT':0,'WK':0,'AR':0,'BOWL':0}
    for d in player_data:
        role = d['tp'].player.role
        idx  = role_counters[role]
        role_counters[role] += 1
        if role == 'BAT' and idx < len(bat_pos):
            d['field_top'], d['field_left'] = bat_pos[idx]
        elif role == 'WK' and idx < len(wk_pos):
            d['field_top'], d['field_left'] = wk_pos[idx]
        elif role == 'AR' and idx < len(ar_pos):
            d['field_top'], d['field_left'] = ar_pos[idx]
        elif role == 'BOWL' and idx < len(bowl_pos):
            d['field_top'], d['field_left'] = bowl_pos[idx]
        else:
            fallback = [('30%','15%'),('30%','85%'),('70%','15%'),('70%','85%'),('50%','8%'),('50%','92%')]
            fi = sum(role_counters.values()) % len(fallback)
            d['field_top'], d['field_left'] = fallback[fi]

    return render(request, 'teams/view_team.html', {
        'tournament': tournament,
        'team': team,
        'player_data': player_data,
    })