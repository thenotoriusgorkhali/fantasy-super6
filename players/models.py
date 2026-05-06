from django.db import models

class Player(models.Model):
    ROLE_CHOICES = [('BAT','Batsman'),('BOWL','Bowler'),('AR','All-Rounder'),('WK','Wicket-Keeper')]
    STYLE_CHOICES = [('Attacking','Attacking'),('Defensive','Defensive'),('Balanced','Balanced')]
    ZONE_CHOICES = [('Off Side','Off Side'),('Leg Side','Leg Side'),('Straight','Straight'),('All Around','All Around')]
    TEAM_CHOICES = [('Team A','Team A'),('Team B','Team B')]

    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50, choices=TEAM_CHOICES)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    price = models.DecimalField(max_digits=4, decimal_places=1, default=8.0)
    playing_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='Balanced')
    batting_rating = models.FloatField(default=5.0)
    bowling_rating = models.FloatField(default=5.0)
    fielding_rating = models.FloatField(default=5.0)
    best_hitting_zone = models.CharField(max_length=20, choices=ZONE_CHOICES, default='All Around')
    profile_image = models.ImageField(upload_to='players/', blank=True, null=True)
    matches_played = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    total_wickets = models.IntegerField(default=0)
    average = models.FloatField(default=0.0)
    strike_rate = models.FloatField(default=0.0)
    economy = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    jersey_number = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['-price', 'name']

    def __str__(self):
        return f"{self.name} ({self.team})"

    def role_color(self):
        colors = {'BAT':'blue','BOWL':'red','AR':'purple','WK':'orange'}
        return colors.get(self.role, 'gray')
