def calculate_points_detailed(performance):
    p = performance
    bd = {}

    # ── BATTING ──
    runs_pts      = p.runs_scored
    boundary_pts  = p.fours
    six_pts       = p.sixes * 2
    milestone     = 16 if p.runs_scored >= 100 else (8 if p.runs_scored >= 50 else 0)
    duck_penalty  = -2 if (p.runs_scored == 0 and p.is_out) else 0

    sr_bonus = 0
    if p.balls_faced >= 10:
        sr = (p.runs_scored / p.balls_faced) * 100
        if   sr >= 170: sr_bonus =  6
        elif sr >= 150: sr_bonus =  4
        elif sr >= 130: sr_bonus =  2
        elif sr <   50: sr_bonus = -6
        elif sr <   60: sr_bonus = -4
        elif sr <   70: sr_bonus = -2

    batting_total = runs_pts + boundary_pts + six_pts + milestone + duck_penalty + sr_bonus

    bd['batting'] = {
        'runs_pts':       runs_pts,
        'boundary_pts':   boundary_pts,
        'six_pts':        six_pts,
        'milestone_bonus': milestone,
        'duck_penalty':   duck_penalty,
        'sr_bonus':       sr_bonus,
        'batting_total':  batting_total,
    }

    # ── BOWLING ──
    wicket_pts   = p.wickets_taken * 25
    maiden_pts   = p.maidens * 8
    wicket_bonus = 16 if p.wickets_taken >= 5 else (8 if p.wickets_taken >= 3 else 0)

    econ_bonus = 0
    if p.overs_bowled >= 2:
        econ = p.runs_conceded / p.overs_bowled if p.overs_bowled > 0 else 0
        if   econ <= 5:  econ_bonus =  6
        elif econ <= 6:  econ_bonus =  4
        elif econ <= 7:  econ_bonus =  2
        elif econ >= 12: econ_bonus = -6
        elif econ >= 11: econ_bonus = -4
        elif econ >= 10: econ_bonus = -2

    bowling_total = wicket_pts + maiden_pts + wicket_bonus + econ_bonus

    bd['bowling'] = {
        'wicket_pts':    wicket_pts,
        'maiden_pts':    maiden_pts,
        'wicket_bonus':  wicket_bonus,
        'economy_bonus': econ_bonus,
        'bowling_total': bowling_total,
    }

    # ── FIELDING ──
    catch_pts   = p.catches    * 8
    stumping_pts = p.stumpings * 12
    runout_pts  = p.run_outs   * 6
    fielding_total = catch_pts + stumping_pts + runout_pts

    bd['fielding'] = {
        'catch_pts':     catch_pts,
        'stumping_pts':  stumping_pts,
        'runout_pts':    runout_pts,
        'fielding_total': fielding_total,
    }

    base = max(batting_total + bowling_total + fielding_total, 0)
    bd['base_points'] = base

    rating = ('Excellent' if base >= 80 else
              'Good'      if base >= 50 else
              'Average'   if base >= 25 else 'Poor')
    bd['performance_rating'] = rating

    return bd


def calculate_points(performance) -> float:
    bd = calculate_points_detailed(performance)
    return bd['base_points']


def apply_multiplier(base_points: float, role_in_team: str) -> float:
    if   role_in_team == 'Captain':      return base_points * 2.0
    elif role_in_team == 'Vice Captain': return base_points * 1.5
    return base_points


def recalculate_team_points(tournament):
    from teams.models import FantasyTeam, FantasyTeamPlayer
    from scoring.models import PlayerPerformance

    performances = {p.player_id: p.base_points
                    for p in PlayerPerformance.objects.filter(tournament=tournament)}

    for ft in FantasyTeam.objects.filter(tournament=tournament):
        total = 0
        for ftp in ft.team_players.all():
            base   = performances.get(ftp.player_id, 0)
            earned = apply_multiplier(base, ftp.role_in_team)
            ftp.points_earned = earned
            ftp.save(update_fields=['points_earned'])
            total += earned
        ft.total_points = total
        ft.save(update_fields=['total_points'])

    for i, team in enumerate(
            FantasyTeam.objects.filter(tournament=tournament).order_by('-total_points'), 1):
        team.rank = i
        team.save(update_fields=['rank'])
