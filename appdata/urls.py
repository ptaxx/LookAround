from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from appdata.views import ActivityView, GamePageView, GamesPageView

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('gamespage/', GamesPageView.as_view(), name='gamespage'),
    path('gamepage/<int:pk>/', GamePageView.as_view(), name='gamepage'),
    path('activitypage/<int:pk>/', ActivityView.as_view(), name='activitypage'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]