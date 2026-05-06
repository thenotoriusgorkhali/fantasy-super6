from django.db import models
from django.utils import timezone

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    team_a_name = models.CharField(max_length=100, default='Thunder XI')
    team_b_name = models.CharField(max_length=100, default='Storm XI')
    match_date = models.DateTimeField()
    deadline = models.DateTimeField()
    venue = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    winner_team = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def is_open(self):
        return timezone.now() < self.deadline

    def time_remaining(self):
        if self.is_open():
            return self.deadline - timezone.now()
        return None

    def status(self):
        if self.is_completed:
            return 'completed'
        now = timezone.now()
        if now < self.deadline:
            return 'open'
        elif now < self.match_date:
            return 'closed'
        return 'closed'
