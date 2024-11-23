from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from appdata.views import (
    ActivityView, 
    GamePageView, 
    GamesPageView, 
    IndexView,
    SignUpView, 
    UserPageViews, 
    game_entry,
    contactpage,
    ActivityCreationFormView
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
    path('signup/', SignUpView.as_view(), name='signup'),
    path('userpage/<int:pk>/', UserPageViews.as_view(), name='userpage'),
    path('creategame', game_entry),
    path('contactpage/', contactpage),
    path('createactivity', ActivityCreationFormView.as_view(), name='createactivity')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

