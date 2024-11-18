from django.urls import path

from appdata.views import GamePageView

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('gamepage/<int:pk>/', GamePageView.as_view(), name="game_page"),
]