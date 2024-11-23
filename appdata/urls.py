from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from appdata.views import (
    ActivityView, 
    GamePageView, 
    GamesPageView, 
    IndexView, 
    UserPageViews, 
    sign_up, 
    game_entry,
    contactpage
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('gamespage/', GamesPageView.as_view(), name='gamespage'),
    path('gamepage/<int:pk>/', GamePageView.as_view(), name='gamepage'),
    path('activitypage/<int:pk>/', ActivityView.as_view(), name='activitypage'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', sign_up),
    path('userpage/<int:pk>/', UserPageViews.as_view(), name='userpage'),
    path('creategame', game_entry),
    path('contactpage/', contactpage),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

