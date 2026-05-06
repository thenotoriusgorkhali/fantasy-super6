from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Tournament
from players.models import Player

class FantasyTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fantasy_teams')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='fantasy_teams')
    team_name = models.CharField(max_length=100)
    total_points = models.FloatField(default=0)
    rank = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'tournament']
        ordering = ['-total_points']

    def __str__(self):
        return f"{self.team_name} by {self.user.username}"

class FantasyTeamPlayer(models.Model):
    ROLE_CHOICES = [('Captain','Captain'),('Vice Captain','Vice Captain'),('Player','Player')]
    fantasy_team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE, related_name='team_players')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    role_in_team = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Player')
    points_earned = models.FloatField(default=0)

    def __str__(self):
        return f"{self.player.name} in {self.fantasy_team.team_name}"
