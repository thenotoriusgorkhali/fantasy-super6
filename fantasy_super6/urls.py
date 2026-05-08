from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as acc_views
from players import views as player_views
from tournaments import views as tour_views
from teams import views as team_views
from scoring import views as score_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tour_views.home, name='home'),
    path('login/', acc_views.login_view, name='login'),
    path('register/', acc_views.register_view, name='register'),
    path('logout/', acc_views.logout_view, name='logout'),
    path('profile/', acc_views.profile_view, name='profile'),
    path('players/', player_views.player_list, name='player_list'),
    path('players/<int:pk>/', player_views.player_detail, name='player_detail'),
    path('tournament/<int:pk>/', tour_views.tournament_detail, name='tournament_detail'),
    path('tournament/<int:tournament_id>/create-team/', team_views.create_team, name='create_team'),
    path('tournament/<int:tournament_id>/my-team/', team_views.my_team, name='my_team'),
    path('tournament/<int:tournament_id>/leaderboard/', score_views.leaderboard, name='leaderboard'),
    path('tournament/<int:tournament_id>/team/<int:team_id>/', score_views.view_team, name='view_team'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)