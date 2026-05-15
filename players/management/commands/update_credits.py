"""
Management command: update_credits
Usage: python manage.py update_credits --tournament <id>

Rules:
  Fantasy Pts >= 150  → +1.0 cr  (exceptional)
  Fantasy Pts >= 100  → +0.5 cr  (great)
  Fantasy Pts >= 60   → +0.0 cr  (decent, no change)
  Fantasy Pts >= 30   → -0.5 cr  (below average)
  Fantasy Pts <  30   → -1.0 cr  (poor)

Hard limits: min 6.0 cr, max 12.0 cr
Rounded to nearest 0.5
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal, ROUND_HALF_UP
from scoring.models import PlayerPerformance
from tournaments.models import Tournament


def round_to_half(val):
    """Round to nearest 0.5"""
    return float(Decimal(str(val * 2)).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / 2)


def credit_delta(fantasy_pts):
    if fantasy_pts >= 150: return  1.0
    if fantasy_pts >= 100: return  0.5
    if fantasy_pts >= 60:  return  0.0
    if fantasy_pts >= 30:  return -0.5
    return -1.0


class Command(BaseCommand):
    help = 'Update player credits based on tournament performance'

    def add_arguments(self, parser):
        parser.add_argument('--tournament', type=int, required=True, help='Tournament ID')
        parser.add_argument('--dry-run', action='store_true', help='Preview changes without saving')

    def handle(self, *args, **options):
        tid = options['tournament']
        dry = options['dry_run']

        try:
            tournament = Tournament.objects.get(pk=tid)
        except Tournament.DoesNotExist:
            self.stderr.write(f'Tournament {tid} not found.')
            return

        perfs = PlayerPerformance.objects.filter(tournament=tournament).select_related('player')
        if not perfs.exists():
            self.stderr.write('No performances found for this tournament.')
            return

        self.stdout.write(f'\n{"DRY RUN — " if dry else ""}Credit update for: {tournament.name}\n')
        self.stdout.write('─' * 62)
        self.stdout.write(f'{"Player":<25} {"Pts":>6} {"Old Cr":>7} {"Δ":>5} {"New Cr":>7}')
        self.stdout.write('─' * 62)

        with transaction.atomic():
            for perf in perfs.order_by('-fantasy_points'):
                player  = perf.player
                pts     = perf.fantasy_points
                old_cr  = float(player.price)
                delta   = credit_delta(pts)
                new_cr  = round_to_half(old_cr + delta)
                new_cr  = max(6.0, min(12.0, new_cr))  # clamp

                arrow = '▲' if delta > 0 else ('▼' if delta < 0 else '─')
                color = self.style.SUCCESS if delta > 0 else (self.style.ERROR if delta < 0 else self.style.WARNING)

                self.stdout.write(
                    f'{player.name:<25} {pts:>6.1f} {old_cr:>6.1f}cr '
                    f'{color(f"{arrow}{abs(delta):.1f}"):>5} {new_cr:>6.1f}cr'
                )

                if not dry:
                    from decimal import Decimal
                    player.price = Decimal(str(new_cr))
                    player.save(update_fields=['price'])

        self.stdout.write('─' * 62)
        if dry:
            self.stdout.write(self.style.WARNING('\nDRY RUN complete — no changes saved. Remove --dry-run to apply.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✓ Credits updated for {perfs.count()} players.'))