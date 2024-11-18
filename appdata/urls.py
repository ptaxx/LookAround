from django.urls import path

from appdata.views import ActivityView, GamePageView

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('gamepage/', GamePageView.as_view(), name="game_page"),
    path('gamepage/<int:pk>/', ActivityView.as_view(), name="activity_page")
]