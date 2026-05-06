import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import FantasyTeam, FantasyTeamPlayer
from players.models import Player
from tournaments.models import Tournament

@login_required
def create_team(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id, is_active=True)
    existing = FantasyTeam.objects.filter(user=request.user, tournament=tournament).first()
    if existing:
        messages.info(request, 'You already have a team for this tournament.')
        return redirect('my_team', tournament_id=tournament_id)
    if not tournament.is_open():
        return render(request, 'teams/closed.html', {'tournament': tournament})

    players = Player.objects.filter(is_active=True).order_by('team', 'role', 'name')

    if request.method == 'POST':
        data = json.loads(request.body)
        team_name   = data.get('team_name', '').strip()
        selected_ids = data.get('players', [])
        captain_id   = data.get('captain')
        vc_id        = data.get('vice_captain')

        errors = []
        if not team_name:           errors.append('Team name is required.')
        if len(selected_ids) != 6:  errors.append('Select exactly 6 players.')
        if not captain_id:          errors.append('Assign a captain.')
        if not vc_id:               errors.append('Assign a vice captain.')
        if captain_id == vc_id:     errors.append('Captain and vice captain must be different.')

        if not errors:
            selected_players = Player.objects.filter(id__in=selected_ids, is_active=True)
            total_price = sum(p.price for p in selected_players)
            if total_price > 60:
                errors.append(f'Budget exceeded: {total_price} > 60 credits.')
            team_a = sum(1 for p in selected_players if p.team == tournament.team_a_name)
            team_b = sum(1 for p in selected_players if p.team == tournament.team_b_name)
            if team_a > 5 or team_b > 5:
                errors.append('Max 5 players from one team.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        ft = FantasyTeam.objects.create(user=request.user, tournament=tournament, team_name=team_name)
        # Points exist already — recalculate for this new team immediately
        _needs_recalc = True
        for pid in selected_ids:
            role = ('Captain'      if str(pid) == str(captain_id) else
                    'Vice Captain' if str(pid) == str(vc_id) else 'Player')
            FantasyTeamPlayer.objects.create(fantasy_team=ft, player_id=pid, role_in_team=role)

        # Recalculate points immediately in case performances already exist
        from scoring.engine import recalculate_team_points
        recalculate_team_points(tournament)

        messages.success(request, f'Team "{team_name}" created! 🎉')
        return JsonResponse({'success': True, 'redirect': f'/tournament/{tournament_id}/my-team/'})

    return render(request, 'teams/create.html', {'tournament': tournament, 'players': players})


@login_required
def my_team(request, tournament_id):
    tournament  = get_object_or_404(Tournament, pk=tournament_id)
    team        = get_object_or_404(FantasyTeam, user=request.user, tournament=tournament)

    from scoring.models import PlayerPerformance
    from scoring.engine import calculate_points_detailed, apply_multiplier

    performances = {p.player_id: p
                    for p in PlayerPerformance.objects.filter(tournament=tournament)}

    # Build rich player data, captain first
    order = {'Captain': 0, 'Vice Captain': 1, 'Player': 2}
    team_players = sorted(team.team_players.select_related('player').all(),
                          key=lambda x: order[x.role_in_team])

    player_data = []
    for tp in team_players:
        perf = performances.get(tp.player_id)
        bd   = None
        multiplier = 2.0 if tp.role_in_team == 'Captain' else (1.5 if tp.role_in_team == 'Vice Captain' else 1.0)

        if perf:
            # Use stored breakdown or recalculate
            bd = perf.points_breakdown or calculate_points_detailed(perf)
            bd['multiplier']   = multiplier
            bd['final_points'] = round(bd['base_points'] * multiplier, 1)
            bd['sr']  = perf.strike_rate()
            bd['eco'] = perf.economy_rate()
        
        # Performance rating colour
        pts = tp.points_earned
        if pts >= 150:   pts_color = '#ffd700'
        elif pts >= 80:  pts_color = '#00e676'
        elif pts >= 40:  pts_color = '#00bcd4'
        else:            pts_color = '#8899aa'

        player_data.append({
            'tp':        tp,
            'perf':      perf,
            'bd':        bd,
            'multiplier': multiplier,
            'pts_color': pts_color,
        })

    # Aggregate summary bars
    bat_total   = sum((d['bd']['batting']['batting_total']  if d['bd'] else 0) for d in player_data)
    bowl_total  = sum((d['bd']['bowling']['bowling_total']  if d['bd'] else 0) for d in player_data)
    field_total = sum((d['bd']['fielding']['fielding_total'] if d['bd'] else 0) for d in player_data)
    bonus_total = sum((
        (d['bd']['batting']['milestone_bonus'] or 0) +
        (d['bd']['bowling']['wicket_bonus'] or 0)
        if d['bd'] else 0) for d in player_data)

    return render(request, 'teams/my_team.html', {
        'tournament':  tournament,
        'team':        team,
        'player_data': player_data,
        'bat_total':   round(bat_total,  1),
        'bowl_total':  round(bowl_total, 1),
        'field_total': round(field_total,1),
        'bonus_total': round(bonus_total,1),
    })
