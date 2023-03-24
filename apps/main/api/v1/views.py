from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class ChessRatingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        url = 'https://api.chess.com/pub/leaderboards'
        response = requests.get(url)
        data = response.json()
        categories = data.keys()
        leaderboard_list = []
        for category in categories:
            for idx, entry in enumerate(data[category]):
                leaderboard = {
                    'category': category,
                    'rank': idx + 1,
                    'username': entry['username'],
                    'rating': entry['score']
                }
                leaderboard_list.append(leaderboard)
        return Response(leaderboard_list)
