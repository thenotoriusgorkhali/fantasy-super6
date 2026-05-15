from django.db import models
import os

def player_image_path(instance, filename):
    ext = filename.split('.')[-1]
    clean = instance.name.lower().replace(' ', '_')
    return f'players/{clean}.{ext}'

class Player(models.Model):
    ROLE_CHOICES  = [('BAT','Batsman'),('BOWL','Bowler'),('AR','All-Rounder'),('WK','Wicket-Keeper')]
    STYLE_CHOICES = [('Attacking','Attacking'),('Defensive','Defensive'),('Balanced','Balanced')]
    ZONE_CHOICES  = [('Off Side','Off Side'),('Leg Side','Leg Side'),('Straight','Straight'),('All Around','All Around')]
    TEAM_CHOICES  = [('Boundary Boys','Boundary Boys'),('Gaule Gugglers','Gaule Gugglers')]

    # ── Core info ──────────────────────────
    name           = models.CharField(max_length=100)
    team           = models.CharField(max_length=50, choices=TEAM_CHOICES)
    role           = models.CharField(max_length=10, choices=ROLE_CHOICES)
    price          = models.DecimalField(max_digits=4, decimal_places=1, default=8.0)
    jersey_number  = models.IntegerField(null=True, blank=True)
    bio            = models.TextField(blank=True)
    profile_image  = models.ImageField(upload_to=player_image_path, blank=True, null=True)
    is_active      = models.BooleanField(default=True)

    # ── Skill ratings ──────────────────────
    batting_rating  = models.FloatField(default=5.0)
    bowling_rating  = models.FloatField(default=5.0)
    fielding_rating = models.FloatField(default=5.0)
    playing_style   = models.CharField(max_length=20, choices=STYLE_CHOICES, default='Balanced')
    best_hitting_zone = models.CharField(max_length=20, choices=ZONE_CHOICES, default='All Around')

    # ── Career batting stats ────────────────
    matches_played  = models.IntegerField(default=0, help_text='Total matches played')
    innings_played  = models.IntegerField(default=0, help_text='Total innings batted')
    total_runs      = models.IntegerField(default=0)
    balls_faced     = models.IntegerField(default=0)
    fours           = models.IntegerField(default=0, help_text='Total boundaries hit')
    sixes           = models.IntegerField(default=0, help_text='Total sixes hit')
    ducks           = models.IntegerField(default=0, help_text='Number of duck dismissals')
    highest_score   = models.IntegerField(default=0, help_text='Highest individual score')
    fifties         = models.IntegerField(default=0, help_text='Number of 50+ scores')
    hundreds        = models.IntegerField(default=0, help_text='Number of 100+ scores')

    # ── Career bowling stats ────────────────
    total_wickets   = models.IntegerField(default=0)
    overs_bowled    = models.FloatField(default=0.0)
    runs_conceded   = models.IntegerField(default=0)
    maidens         = models.IntegerField(default=0)
    best_bowling_wkts = models.IntegerField(default=0, help_text='Best bowling wickets')
    best_bowling_runs = models.IntegerField(default=999, help_text='Best bowling runs conceded')

    # ── Career fielding stats ───────────────
    catches         = models.IntegerField(default=0)
    stumpings       = models.IntegerField(default=0)
    run_outs        = models.IntegerField(default=0)
    missed_catches  = models.IntegerField(default=0, help_text='Dropped catches')

    # ── Fantasy stats ───────────────────────
    total_fantasy_points = models.FloatField(default=0.0, help_text='Cumulative fantasy points')

    class Meta:
        ordering = ['-price', 'name']

    def __str__(self):
        return f"{self.name} ({self.team})"

    # ── Computed properties ─────────────────
    @property
    def career_average(self):
        if self.innings_played > 0:
            return round(self.total_runs / self.innings_played, 1)
        return 0.0

    @property
    def career_strike_rate(self):
        if self.balls_faced > 0:
            return round(self.total_runs / self.balls_faced * 100, 1)
        return 0.0

    @property
    def career_economy(self):
        if self.overs_bowled > 0:
            return round(self.runs_conceded / self.overs_bowled, 1)
        return 0.0

    @property
    def avg_fantasy_per_match(self):
        if self.matches_played > 0:
            return round(self.total_fantasy_points / self.matches_played, 1)
        return 0.0

    @property
    def best_bowling_str(self):
        if self.best_bowling_wkts > 0:
            return f"{self.best_bowling_wkts}/{self.best_bowling_runs}"
        return "—"

    def role_color(self):
        return {'BAT':'blue','BOWL':'red','AR':'purple','WK':'orange'}.get(self.role,'gray')