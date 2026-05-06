# ⚡ Fantasy Super 6

A premium local cricket fantasy web app built with Django — Dream11 level quality for your local matches.

## 🏏 Features
- Pick 6 players from both teams within 60 credits
- Assign Captain (2×) and Vice Captain (1.5×) multipliers
- Real-time countdown timer for team selection deadline
- Automatic points calculation from match performances
- Live leaderboard with podium display
- Beautiful dark theme with glassmorphism cards
- Fully responsive design (mobile + desktop)

## 🚀 Quick Setup

```bash
# 1. Clone / download the project
cd fantasy_super6

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Seed sample data (players, tournament, test users)
python manage.py seed_data

# 6. Run the development server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

## 👤 Test Accounts
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Superuser (admin panel) |
| player1 | pass123 | Regular user |
| player2 | pass123 | Regular user |

**Admin Panel:** http://127.0.0.1:8000/admin/

## 📋 How to Add Players
1. Go to Admin Panel → Players → Add Player
2. Fill in: Name, Team (Thunder XI / Storm XI), Role, Price, Ratings, Stats
3. Set `Is Active` = True

## 📊 How to Enter Match Scores
1. Admin Panel → **Player Performances** → Add Performance
2. Select Player + Tournament
3. Enter batting stats (runs, balls, fours, sixes, is_out)
4. Enter bowling stats (overs, wickets, runs conceded, maidens)
5. Enter fielding stats (catches, run outs, stumpings)
6. **Save** — points are auto-calculated!
7. Fantasy team points and ranks are automatically updated.

## 🔗 URL Reference
| URL | Page |
|-----|------|
| `/` | Home (tournament overview + countdown) |
| `/players/` | Player browser with filters |
| `/players/<id>/` | Individual player profile |
| `/login/` | Login |
| `/register/` | Register |
| `/profile/` | User profile & team history |
| `/tournament/<id>/create-team/` | Create fantasy team |
| `/tournament/<id>/my-team/` | View your team |
| `/tournament/<id>/leaderboard/` | Full leaderboard |
| `/admin/` | Django admin panel |

## 🎯 Scoring System
**Batting:** +1/run, +1/four, +2/six, +8 (50+ bonus), +16 (100+ bonus), -2 duck  
**Bowling:** +25/wicket, +8/maiden, +8 (3-wkt bonus), +16 (5-wkt bonus)  
**Fielding:** +8/catch, +12/stumping, +6/run-out  
**Captain:** 2× multiplier | **Vice Captain:** 1.5× multiplier

## 🛠 Tech Stack
- **Backend:** Django 4.2, Python 3.11, SQLite
- **Frontend:** Tailwind CSS, Alpine.js, Lucide Icons
- **Auth:** Django built-in auth + django-allauth
