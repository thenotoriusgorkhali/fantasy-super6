from .models import Tournament

def active_tournament(request):
    tournament = Tournament.objects.filter(is_active=True).order_by('-created_at').first()
    return {'active_tournament': tournament}
