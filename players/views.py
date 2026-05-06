from django.shortcuts import render, get_object_or_404
from .models import Player
from scoring.models import PlayerPerformance

def player_list(request):
    players = Player.objects.filter(is_active=True)
    return render(request, 'players/list.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk, is_active=True)
    performances = PlayerPerformance.objects.filter(player=player).select_related('tournament').order_by('-tournament__match_date')[:10]
    return render(request, 'players/detail.html', {'player': player, 'performances': performances})
