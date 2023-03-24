from django.urls import path

from apps.main.api.v1.views import ChessRatingAPIView

urlpatterns = [
    path('chess/ratings/', ChessRatingAPIView.as_view(), name='chess_ratings')
]
