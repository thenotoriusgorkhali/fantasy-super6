from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        from players.models import Player
        from tournaments.models import Tournament
        from teams.models import FantasyTeam, FantasyTeamPlayer
        from accounts.models import UserProfile
        
        # Create players
        Player.objects.all().delete()
        
        thunder_players = [
            {'name': 'Rohit Shrestha', 'role': 'BAT', 'price': 10.5, 'style': 'Attacking', 'jersey': 45,
             'bat_r': 9.2, 'bowl_r': 2.0, 'field_r': 7.5, 'zone': 'Off Side',
             'matches': 42, 'runs': 1820, 'wickets': 3, 'avg': 43.3, 'sr': 145.0, 'economy': 0,
             'bio': 'Explosive opener known for his big hits and consistent performances.'},
            {'name': 'Aarav Karmacharya', 'role': 'BOWL', 'price': 9.0, 'style': 'Defensive', 'jersey': 7,
             'bat_r': 3.5, 'bowl_r': 8.8, 'field_r': 6.0, 'zone': 'Straight',
             'matches': 38, 'runs': 210, 'wickets': 72, 'avg': 15.2, 'sr': 65.0, 'economy': 5.8,
             'bio': 'Crafty medium pacer with exceptional control and swing.'},
            {'name': 'Dipesh Gurung', 'role': 'AR', 'price': 9.5, 'style': 'Balanced', 'jersey': 23,
             'bat_r': 7.5, 'bowl_r': 7.2, 'field_r': 8.0, 'zone': 'All Around',
             'matches': 50, 'runs': 1150, 'wickets': 48, 'avg': 32.0, 'sr': 120.0, 'economy': 6.5,
             'bio': 'Versatile all-rounder who contributes equally with bat and ball.'},
            {'name': 'Sagar Malla', 'role': 'WK', 'price': 9.0, 'style': 'Attacking', 'jersey': 12,
             'bat_r': 8.0, 'bowl_r': 1.0, 'field_r': 9.0, 'zone': 'Leg Side',
             'matches': 45, 'runs': 1340, 'wickets': 0, 'avg': 38.5, 'sr': 135.0, 'economy': 0,
             'bio': 'Aggressive wicket-keeper batsman with lightning reflexes behind the stumps.'},
            {'name': 'Bikash Tamang', 'role': 'BAT', 'price': 8.5, 'style': 'Balanced', 'jersey': 3,
             'bat_r': 7.8, 'bowl_r': 1.5, 'field_r': 7.0, 'zone': 'Off Side',
             'matches': 35, 'runs': 980, 'wickets': 2, 'avg': 35.0, 'sr': 118.0, 'economy': 0,
             'bio': 'Stylish middle-order batsman known for building crucial partnerships.'},
            {'name': 'Nabin Maharjan', 'role': 'BOWL', 'price': 8.0, 'style': 'Attacking', 'jersey': 18,
             'bat_r': 4.0, 'bowl_r': 8.2, 'field_r': 6.5, 'zone': 'Straight',
             'matches': 30, 'runs': 125, 'wickets': 55, 'avg': 18.5, 'sr': 72.0, 'economy': 6.2,
             'bio': 'Aggressive fast bowler who consistently generates pace and bounce.'},
            {'name': 'Pratik Joshi', 'role': 'AR', 'price': 8.5, 'style': 'Attacking', 'jersey': 31,
             'bat_r': 7.0, 'bowl_r': 6.8, 'field_r': 7.5, 'zone': 'Leg Side',
             'matches': 28, 'runs': 620, 'wickets': 32, 'avg': 28.0, 'sr': 130.0, 'economy': 7.1,
             'bio': 'Dynamic all-rounder who excels in high-pressure situations.'},
            {'name': 'Suraj Thapa', 'role': 'BAT', 'price': 7.5, 'style': 'Defensive', 'jersey': 56,
             'bat_r': 7.2, 'bowl_r': 1.0, 'field_r': 6.0, 'zone': 'Off Side',
             'matches': 22, 'runs': 540, 'wickets': 0, 'avg': 30.0, 'sr': 105.0, 'economy': 0,
             'bio': 'Compact opener who provides stability at the top of the order.'},
        ]
        
        storm_players = [
            {'name': 'Kiran Adhikari', 'role': 'BAT', 'price': 10.0, 'style': 'Attacking', 'jersey': 99,
             'bat_r': 9.0, 'bowl_r': 2.5, 'field_r': 8.0, 'zone': 'All Around',
             'matches': 48, 'runs': 2100, 'wickets': 5, 'avg': 52.5, 'sr': 158.0, 'economy': 0,
             'bio': "Storm's captain and premier batsman with an incredible record at the top."},
            {'name': 'Manish Pradhan', 'role': 'BOWL', 'price': 9.5, 'style': 'Attacking', 'jersey': 77,
             'bat_r': 4.5, 'bowl_r': 9.1, 'field_r': 7.0, 'zone': 'Straight',
             'matches': 40, 'runs': 180, 'wickets': 85, 'avg': 14.0, 'sr': 60.0, 'economy': 5.5,
             'bio': 'Premier wicket-taker known for his deadly yorkers and reverse swing.'},
            {'name': 'Rajesh Bhandari', 'role': 'AR', 'price': 9.0, 'style': 'Balanced', 'jersey': 14,
             'bat_r': 7.8, 'bowl_r': 7.5, 'field_r': 8.5, 'zone': 'All Around',
             'matches': 45, 'runs': 1080, 'wickets': 42, 'avg': 29.0, 'sr': 125.0, 'economy': 6.8,
             'bio': 'Seasoned all-rounder who reads the game exceptionally well.'},
            {'name': 'Anil Shahi', 'role': 'WK', 'price': 8.5, 'style': 'Balanced', 'jersey': 22,
             'bat_r': 7.5, 'bowl_r': 1.0, 'field_r': 9.2, 'zone': 'Leg Side',
             'matches': 38, 'runs': 1100, 'wickets': 0, 'avg': 35.0, 'sr': 128.0, 'economy': 0,
             'bio': 'Technically sound keeper-batsman with exceptional glovework.'},
            {'name': 'Gaurav Pant', 'role': 'BAT', 'price': 9.0, 'style': 'Attacking', 'jersey': 66,
             'bat_r': 8.5, 'bowl_r': 1.5, 'field_r': 7.5, 'zone': 'All Around',
             'matches': 32, 'runs': 1250, 'wickets': 1, 'avg': 48.0, 'sr': 162.0, 'economy': 0,
             'bio': 'Explosive middle-order dasher capable of turning matches single-handedly.'},
            {'name': 'Prashant KC', 'role': 'BOWL', 'price': 8.0, 'style': 'Defensive', 'jersey': 8,
             'bat_r': 3.0, 'bowl_r': 8.5, 'field_r': 6.0, 'zone': 'Off Side',
             'matches': 28, 'runs': 95, 'wickets': 52, 'avg': 16.5, 'sr': 65.0, 'economy': 6.0,
             'bio': 'Reliable spinner who ties down batsmen with consistent accuracy.'},
            {'name': 'Aakash Bista', 'role': 'AR', 'price': 8.5, 'style': 'Attacking', 'jersey': 41,
             'bat_r': 6.8, 'bowl_r': 7.0, 'field_r': 7.8, 'zone': 'Leg Side',
             'matches': 25, 'runs': 580, 'wickets': 28, 'avg': 27.0, 'sr': 132.0, 'economy': 7.0,
             'bio': 'Young talent who has impressed with his fearless approach to the game.'},
            {'name': 'Tej Mijar', 'role': 'BAT', 'price': 7.0, 'style': 'Defensive', 'jersey': 88,
             'bat_r': 6.5, 'bowl_r': 2.0, 'field_r': 6.5, 'zone': 'Off Side',
             'matches': 18, 'runs': 420, 'wickets': 3, 'avg': 28.0, 'sr': 100.0, 'economy': 8.5,
             'bio': 'Solid defensive batsman who anchors the innings under pressure.'},
        ]
        
        for pd in thunder_players:
            Player.objects.create(
                name=pd['name'], team='Thunder XI', role=pd['role'], price=pd['price'],
                playing_style=pd['style'], jersey_number=pd['jersey'],
                batting_rating=pd['bat_r'], bowling_rating=pd['bowl_r'], fielding_rating=pd['field_r'],
                best_hitting_zone=pd['zone'], matches_played=pd['matches'],
                total_runs=pd['runs'], total_wickets=pd['wickets'],
                average=pd['avg'], strike_rate=pd['sr'], economy=pd['economy'],
                bio=pd['bio'], is_active=True
            )
        
        for pd in storm_players:
            Player.objects.create(
                name=pd['name'], team='Storm XI', role=pd['role'], price=pd['price'],
                playing_style=pd['style'], jersey_number=pd['jersey'],
                batting_rating=pd['bat_r'], bowling_rating=pd['bowl_r'], fielding_rating=pd['field_r'],
                best_hitting_zone=pd['zone'], matches_played=pd['matches'],
                total_runs=pd['runs'], total_wickets=pd['wickets'],
                average=pd['avg'], strike_rate=pd['sr'], economy=pd['economy'],
                bio=pd['bio'], is_active=True
            )
        
        self.stdout.write(f'✓ Created {Player.objects.count()} players')
        
        # Create tournament
        Tournament.objects.all().delete()
        tournament = Tournament.objects.create(
            name='Fantasy Super 6 — Season 1',
            team_a_name='Thunder XI',
            team_b_name='Storm XI',
            match_date=timezone.now() + timedelta(hours=26),
            deadline=timezone.now() + timedelta(hours=24),
            venue='Tribhuvan University Ground, Kathmandu',
            description='The inaugural season of Fantasy Super 6!',
            is_active=True,
        )
        self.stdout.write(f'✓ Created tournament: {tournament.name}')
        
        # Create users
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@fantasy.com', 'admin123')
            UserProfile.objects.get_or_create(user=admin)
        
        for uname, email, pwd in [('player1', 'p1@fantasy.com', 'pass123'), ('player2', 'p2@fantasy.com', 'pass123')]:
            if not User.objects.filter(username=uname).exists():
                u = User.objects.create_user(uname, email, pwd)
                UserProfile.objects.get_or_create(user=u)
        
        self.stdout.write('✓ Created users: admin/admin123, player1/pass123, player2/pass123')
        
        # Create sample teams
        FantasyTeam.objects.all().delete()
        players = list(Player.objects.all())
        thunder = [p for p in players if p.team == 'Thunder XI']
        storm = [p for p in players if p.team == 'Storm XI']
        
        for uname, tname in [('player1', 'Team Rocket'), ('player2', 'Champions XI')]:
            user = User.objects.get(username=uname)
            # Pick 3 from each team
            selection = random.sample(thunder, 3) + random.sample(storm, 3)
            ft = FantasyTeam.objects.create(user=user, tournament=tournament, team_name=tname)
            for i, p in enumerate(selection):
                role = 'Captain' if i == 0 else ('Vice Captain' if i == 1 else 'Player')
                FantasyTeamPlayer.objects.create(fantasy_team=ft, player=p, role_in_team=role)
        
        self.stdout.write('✓ Created sample fantasy teams')
        self.stdout.write(self.style.SUCCESS('\n✅ Seed data created successfully!'))
        self.stdout.write('  Run: python manage.py runserver')
        self.stdout.write('  Visit: http://127.0.0.1:8000/')
