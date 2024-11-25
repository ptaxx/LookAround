from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from appdata.views import (
    ActivityView,
    AreaPageView, 
    GamePageView, 
    GamesPageView, 
    IndexView, 
    UserPageViews, 
    SignUpView, 
    GameEntryView,
    ContactPage,
    ActivityCreationFormView,
    VenuePageView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('areapage/<int:pk>/', AreaPageView.as_view(), name='areapage'),
    path('venuepage/<int:pk>/', VenuePageView.as_view(), name='venuepage'),
    path('gamespage/', GamesPageView.as_view(), name='gamespage'),
    path('gamepage/<int:pk>/', GamePageView.as_view(), name='gamepage'),
    path('activitypage/<int:pk>/', ActivityView.as_view(), name='activitypage'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('userpage/<int:pk>/', UserPageViews.as_view(), name='userpage'),
    path('createactivity', ActivityCreationFormView.as_view(), name='createactivity'),
    path('creategame', GameEntryView.as_view(), name='index'),
    path('contactpage/', ContactPage.as_view(), name='contact'),
    path('createactivity', ActivityCreationFormView.as_view(), name='createactivity')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

