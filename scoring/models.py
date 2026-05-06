from django.db import models
from players.models import Player
from tournaments.models import Tournament

class PlayerPerformance(models.Model):
    player       = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='performances')
    tournament   = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='performances')
    runs_scored  = models.IntegerField(default=0)
    balls_faced  = models.IntegerField(default=0)
    fours        = models.IntegerField(default=0)
    sixes        = models.IntegerField(default=0)
    is_out       = models.BooleanField(default=True)
    overs_bowled = models.FloatField(default=0)
    wickets_taken= models.IntegerField(default=0)
    runs_conceded= models.IntegerField(default=0)
    maidens      = models.IntegerField(default=0)
    catches      = models.IntegerField(default=0)
    run_outs     = models.IntegerField(default=0)
    stumpings    = models.IntegerField(default=0)
    base_points  = models.FloatField(default=0)
    fantasy_points = models.FloatField(default=0)
    notes        = models.TextField(blank=True)
    points_breakdown = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ['player', 'tournament']

    def __str__(self):
        return f"{self.player.name} — {self.tournament.name}"

    def save(self, *args, **kwargs):
        from scoring.engine import calculate_points_detailed, recalculate_team_points
        bd = calculate_points_detailed(self)
        self.base_points     = bd['base_points']
        self.fantasy_points  = bd['base_points']
        self.points_breakdown = bd
        super().save(*args, **kwargs)
        recalculate_team_points(self.tournament)

    def strike_rate(self):
        if self.balls_faced > 0:
            return round((self.runs_scored / self.balls_faced) * 100, 1)
        return 0.0

    def economy_rate(self):
        if self.overs_bowled > 0:
            return round(self.runs_conceded / self.overs_bowled, 1)
        return 0.0
