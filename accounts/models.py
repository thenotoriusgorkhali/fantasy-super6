from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    total_tournaments_played = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    favorite_player = models.ForeignKey('players.Player', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def initials(self):
        parts = self.user.get_full_name().split() or [self.user.username]
        return ''.join(p[0].upper() for p in parts[:2])
