from django.shortcuts import render, get_object_or_404
from .models import Player
from scoring.models import PlayerPerformance

def player_list(request):
    players = Player.objects.filter(is_active=True)

    for player in players:
        if player.matches_played > 0:
            player.career_avg = player.career_average
            player.career_sr  = player.career_strike_rate
        else:
            player.career_avg = 0
            player.career_sr  = 0

    return render(request, 'players/list.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk, is_active=True)
    performances = PlayerPerformance.objects.filter(player=player).select_related('tournament').order_by('-tournament__match_date')

    # Use model's own career stats (manually maintained by admin)
    # Fall back to computing from performances if model stats are zero
    if player.matches_played > 0:
        # Admin has filled in career stats — use them directly
        total_runs    = player.total_runs
        total_wkts    = player.total_wickets
        total_catches = player.catches + player.stumpings
        total_fours   = player.fours
        total_sixes   = player.sixes
        fifties       = player.fifties
        hundreds      = player.hundreds
        matches       = player.matches_played
        innings       = player.innings_played
        ducks         = player.ducks
        missed        = player.missed_catches
        run_outs      = player.run_outs
        maidens       = player.maidens
        career_avg    = player.career_average
        career_sr     = player.career_strike_rate
        career_eco    = player.career_economy
        best_score    = f"{player.highest_score}*" if player.highest_score > 0 else "—"
        best_bowling  = player.best_bowling_str
        total_fp      = player.total_fantasy_points
        avg_fp        = player.avg_fantasy_per_match
    else:
        # Compute from match performances
        total_runs = balls = total_wkts = overs = rc = 0
        total_catches = total_fours = total_sixes = 0
        fifties = hundreds = ducks = missed = run_outs = maidens = 0
        best_score_num = 0; best_score_out = True
        best_bowling_wkts = 0; best_bowling_runs = 999
        total_fp = 0; matches = performances.count(); innings = 0

        for p in performances:
            total_runs  += p.runs_scored
            balls       += p.balls_faced
            total_wkts  += p.wickets_taken
            overs       += p.overs_bowled
            rc          += p.runs_conceded
            total_catches += p.catches + p.stumpings
            total_fours += p.fours
            total_sixes += p.sixes
            total_fp    += p.fantasy_points
            maidens     += p.maidens
            run_outs    += p.run_outs
            if p.runs_scored >= 100: hundreds += 1
            if p.runs_scored >= 50:  fifties  += 1
            if p.runs_scored > best_score_num:
                best_score_num = p.runs_scored
                best_score_out = p.is_out
            if p.wickets_taken > best_bowling_wkts or (p.wickets_taken == best_bowling_wkts and p.runs_conceded < best_bowling_runs and p.wickets_taken > 0):
                best_bowling_wkts = p.wickets_taken
                best_bowling_runs = p.runs_conceded

        innings    = matches
        career_avg = round(total_runs / matches, 1) if matches > 0 else 0
        career_sr  = round(total_runs / balls * 100, 1) if balls > 0 else 0
        career_eco = round(rc / overs, 1) if overs > 0 else 0
        avg_fp     = round(total_fp / matches, 1) if matches > 0 else 0
        best_score = f"{best_score_num}{'*' if not best_score_out else ''}" if best_score_num > 0 else "—"
        best_bowling = f"{best_bowling_wkts}/{best_bowling_runs}" if best_bowling_wkts > 0 else "—"
        ducks = missed = 0

    # Dynamic badges
    badges = []
    if avg_fp >= 150:
        badges.append({'icon':'👑','text':'Fantasy King','color':'#ffd700','bg':'rgba(255,215,0,0.12)','border':'rgba(255,215,0,0.3)'})
    elif avg_fp >= 100:
        badges.append({'icon':'⭐','text':'Fantasy Elite','color':'#00e676','bg':'rgba(0,230,118,0.12)','border':'rgba(0,230,118,0.3)'})
    elif avg_fp >= 60:
        badges.append({'icon':'🔥','text':'Hot Pick','color':'#fb923c','bg':'rgba(249,115,22,0.12)','border':'rgba(249,115,22,0.3)'})
    if player.highest_score >= 100 or hundreds >= 1:
        badges.append({'icon':'💯','text':'Century Maker','color':'#fcd34d','bg':'rgba(252,211,77,0.12)','border':'rgba(252,211,77,0.3)'})
    elif player.highest_score >= 75 or (best_score != '—' and best_score.replace('*','').isdigit() and int(best_score.replace('*','')) >= 75):
        badges.append({'icon':'🏏','text':'Big Hitter','color':'#60a5fa','bg':'rgba(96,165,250,0.12)','border':'rgba(96,165,250,0.3)'})
    if career_sr >= 160:
        badges.append({'icon':'💥','text':'Power Striker','color':'#f87171','bg':'rgba(248,113,113,0.12)','border':'rgba(248,113,113,0.3)'})
    elif career_sr >= 130:
        badges.append({'icon':'⚡','text':'Explosive Batter','color':'#fb923c','bg':'rgba(249,115,22,0.12)','border':'rgba(249,115,22,0.3)'})
    if total_wkts >= 5:
        badges.append({'icon':'🎳','text':'Wicket Machine','color':'#f87171','bg':'rgba(248,113,113,0.12)','border':'rgba(248,113,113,0.3)'})
    elif total_wkts >= 3:
        badges.append({'icon':'🎯','text':'Key Bowler','color':'#fb923c','bg':'rgba(249,115,22,0.12)','border':'rgba(249,115,22,0.3)'})
    if career_eco > 0 and career_eco <= 6:
        badges.append({'icon':'🧊','text':'Economy Master','color':'#00bcd4','bg':'rgba(0,188,212,0.12)','border':'rgba(0,188,212,0.3)'})
    if total_catches >= 3:
        badges.append({'icon':'🧤','text':'Safe Hands','color':'#c4b5fd','bg':'rgba(196,181,253,0.12)','border':'rgba(196,181,253,0.3)'})
    if player.batting_rating >= 9:
        badges.append({'icon':'🏆','text':'Elite Batsman','color':'#3b82f6','bg':'rgba(59,130,246,0.12)','border':'rgba(59,130,246,0.3)'})
    if player.bowling_rating >= 9:
        badges.append({'icon':'🔴','text':'Elite Bowler','color':'#ef4444','bg':'rgba(239,68,68,0.12)','border':'rgba(239,68,68,0.3)'})
    if player.role == 'AR':
        badges.append({'icon':'⚡','text':'All-Round Threat','color':'#a78bfa','bg':'rgba(167,139,250,0.12)','border':'rgba(167,139,250,0.3)'})
    badges = badges[:5]

    context = {
        'player': player,
        'performances': performances,
        'badges': badges,
        # Career stats
        'matches': matches,
        'innings': innings,
        'total_runs': total_runs,
        'total_wkts': total_wkts,
        'total_catches': total_catches,
        'total_fours': total_fours,
        'total_sixes': total_sixes,
        'fifties': fifties,
        'hundreds': hundreds,
        'ducks': ducks,
        'missed_catches': missed,
        'run_outs': run_outs,
        'maidens': maidens,
        'career_avg': career_avg,
        'career_sr': career_sr,
        'career_eco': career_eco,
        'best_score': best_score,
        'best_bowling': best_bowling,
        'total_fantasy_pts': round(total_fp, 1),
        'avg_fantasy': avg_fp,
    }
    return render(request, 'players/detail.html', context)