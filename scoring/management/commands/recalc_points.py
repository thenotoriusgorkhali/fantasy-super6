from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Recalculate fantasy points for ALL teams in ALL tournaments'

    def handle(self, *args, **kwargs):
        from scoring.engine import recalculate_team_points
        from tournaments.models import Tournament
        from teams.models import FantasyTeam

        for t in Tournament.objects.all():
            self.stdout.write(f'Processing: {t.name}')
            recalculate_team_points(t)
            for ft in FantasyTeam.objects.filter(tournament=t).order_by('-total_points'):
                self.stdout.write(f'  #{ft.rank} {ft.team_name} ({ft.user.username}) → {ft.total_points:.1f} pts')

        self.stdout.write(self.style.SUCCESS('\n✅ All points recalculated! Refresh your browser.'))