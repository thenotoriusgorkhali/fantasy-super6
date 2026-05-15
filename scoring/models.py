from django.db import models
from players.models import Player
from tournaments.models import Tournament

class PlayerPerformance(models.Model):
    player        = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='performances')
    tournament    = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='performances')

    # Match info
    matches_played = models.IntegerField(default=1, help_text='Number of matches played in this tournament day')
    innings_played = models.IntegerField(default=1, help_text='Number of innings batted')

    # Batting — cumulative totals for the tournament day
    runs_scored   = models.IntegerField(default=0, help_text='Total runs across all matches')
    balls_faced   = models.IntegerField(default=0)
    fours         = models.IntegerField(default=0)
    sixes         = models.IntegerField(default=0)
    is_out        = models.BooleanField(default=True, help_text='Was out at least once (for duck calculation)')

    # Best score in a single innings
    best_score_runs = models.IntegerField(default=0, help_text='Highest score in a single innings')
    best_score_not_out = models.BooleanField(default=False, help_text='Was not out in that best innings?')
    ducks           = models.IntegerField(default=0, help_text='Number of duck dismissals (0 runs, out)')

    # Bowling — cumulative
    overs_bowled  = models.FloatField(default=0)
    wickets_taken = models.IntegerField(default=0, help_text='Total wickets across all matches')
    runs_conceded = models.IntegerField(default=0)
    maidens       = models.IntegerField(default=0)

    # Best bowling in a single spell
    best_bowling_wkts = models.IntegerField(default=0, help_text='Best bowling wickets in one match')
    best_bowling_runs = models.IntegerField(default=0, help_text='Runs conceded in that best bowling spell')

    # Fielding
    catches       = models.IntegerField(default=0)
    run_outs      = models.IntegerField(default=0)
    stumpings     = models.IntegerField(default=0)
    missed_catches = models.IntegerField(default=0, help_text='Dropped catches — each deducts 5 pts')

    # Fantasy points
    base_points      = models.FloatField(default=0)
    fantasy_points   = models.FloatField(default=0)
    notes            = models.TextField(blank=True)
    points_breakdown = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ['player', 'tournament']

    def __str__(self):
        return f"{self.player.name} — {self.tournament.name}"

    def save(self, *args, **kwargs):
        from scoring.engine import calculate_points_detailed, recalculate_team_points

        # Calculate fantasy points
        bd = calculate_points_detailed(self)
        self.base_points      = bd['base_points']
        self.fantasy_points   = bd['base_points']
        self.points_breakdown = bd
        super().save(*args, **kwargs)

        # ── Auto-update Player career stats ──────────────────────
        self._sync_player_career_stats()

        # Recalculate fantasy team points
        recalculate_team_points(self.tournament)

    def _sync_player_career_stats(self):
        """Recompute player's career totals from all performances."""
        player = self.player
        all_perfs = PlayerPerformance.objects.filter(player=player)

        # Aggregate
        total_runs = total_balls = total_fours = total_sixes = 0
        total_wkts = total_rc = total_maidens = 0
        total_overs = 0.0
        total_catches = total_stumpings = total_run_outs = total_missed = 0
        total_fp = 0.0
        fifties = hundreds = ducks = 0
        best_score = 0
        best_wkts = 0; best_runs = 999
        innings = matches = 0

        for p in all_perfs:
            matches        += p.matches_played
            innings        += p.innings_played
            total_runs     += p.runs_scored
            total_balls    += p.balls_faced
            total_fours    += p.fours
            total_sixes    += p.sixes
            total_wkts     += p.wickets_taken
            total_rc       += p.runs_conceded
            total_overs    += p.overs_bowled
            total_maidens  += p.maidens
            total_catches  += p.catches
            total_stumpings += p.stumpings
            total_run_outs += p.run_outs
            total_missed   += p.missed_catches
            total_fp       += p.fantasy_points
            ducks          += p.ducks

            # Count milestones from best_score field
            if p.best_score_runs >= 100: hundreds += 1
            elif p.best_score_runs >= 50: fifties  += 1

            # Track best score
            if p.best_score_runs > best_score: best_score = p.best_score_runs

            # Track best bowling
            if p.best_bowling_wkts > best_wkts or (p.best_bowling_wkts == best_wkts and p.best_bowling_runs < best_runs and p.best_bowling_wkts > 0):
                best_wkts = p.best_bowling_wkts
                best_runs = p.best_bowling_runs

        # Update player model
        player.matches_played       = matches
        player.innings_played       = innings
        player.total_runs           = total_runs
        player.balls_faced          = total_balls
        player.fours                = total_fours
        player.sixes                = total_sixes
        player.total_wickets        = total_wkts
        player.runs_conceded        = total_rc
        player.overs_bowled         = round(total_overs, 1)
        player.maidens              = total_maidens
        player.catches              = total_catches
        player.stumpings            = total_stumpings
        player.run_outs             = total_run_outs
        player.missed_catches       = total_missed
        player.total_fantasy_points = round(total_fp, 1)
        player.fifties              = fifties
        player.hundreds             = hundreds
        player.ducks                = ducks
        player.highest_score        = best_score
        player.best_bowling_wkts    = best_wkts
        player.best_bowling_runs    = best_runs if best_wkts > 0 else 999
        player.save()

    def strike_rate(self):
        if self.balls_faced > 0:
            return round((self.runs_scored / self.balls_faced) * 100, 1)
        return 0.0

    def economy_rate(self):
        if self.overs_bowled > 0:
            return round(self.runs_conceded / self.overs_bowled, 1)
        return 0.0