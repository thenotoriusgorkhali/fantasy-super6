from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from .models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'team_a_name', 'team_b_name', 'match_date', 'is_active', 'is_completed']
    list_filter   = ['is_active', 'is_completed']
    actions       = ['preview_credit_update', 'apply_credit_update']

    def preview_credit_update(self, request, queryset):
        from scoring.models import PlayerPerformance
        from decimal import Decimal, ROUND_HALF_UP

        def round_half(v):
            return float(Decimal(str(v*2)).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / 2)

        def delta(pts):
            if pts >= 150: return  1.0
            if pts >= 100: return  0.5
            if pts >= 60:  return  0.0
            if pts >= 30:  return -0.5
            return -1.0

        lines = []
        for t in queryset:
            perfs = PlayerPerformance.objects.filter(tournament=t).select_related('player').order_by('-fantasy_points')
            if not perfs:
                lines.append(f'No performances for {t.name}')
                continue
            lines.append(f'<strong>{t.name}</strong>')
            for p in perfs:
                old = float(p.player.price)
                d   = delta(p.fantasy_points)
                new = max(6.0, min(12.0, round_half(old + d)))
                arrow = '▲' if d > 0 else ('▼' if d < 0 else '─')
                color = '#00a854' if d > 0 else ('#f5222d' if d < 0 else '#888')
                lines.append(
                    f'&nbsp;&nbsp;{p.player.name}: {p.fantasy_points:.0f}pts → '
                    f'<span style="color:{color};font-weight:700">{arrow} {old:.1f}cr → {new:.1f}cr</span>'
                )
        self.message_user(request, format_html('<br>'.join(lines)), level=messages.INFO)
    preview_credit_update.short_description = '👁 Preview credit changes (no save)'

    def apply_credit_update(self, request, queryset):
        from scoring.models import PlayerPerformance
        from decimal import Decimal, ROUND_HALF_UP

        def round_half(v):
            return float(Decimal(str(v*2)).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / 2)

        def delta(pts):
            if pts >= 150: return  1.0
            if pts >= 100: return  0.5
            if pts >= 60:  return  0.0
            if pts >= 30:  return -0.5
            return -1.0

        total = 0
        for t in queryset:
            perfs = PlayerPerformance.objects.filter(tournament=t).select_related('player')
            for p in perfs:
                old = float(p.player.price)
                d   = delta(p.fantasy_points)
                new = max(6.0, min(12.0, round_half(old + d)))
                p.player.price = Decimal(str(new))
                p.player.save(update_fields=['price'])
                total += 1
        self.message_user(request, f'✅ Credits updated for {total} players.', level=messages.SUCCESS)
    apply_credit_update.short_description = '💾 Apply credit update (saves to DB)'