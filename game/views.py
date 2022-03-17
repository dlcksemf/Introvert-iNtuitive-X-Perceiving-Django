from django.db.models import Q
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from game.models import Game, LoanedGame
from game.serializers import GameSerializer,LoanedGameSerializer,LoanedGameCreationSerializer
from game.paginations.GamePagination import GamePagination


class GameViewSet(ModelViewSet):
    queryset=Game.objects.all()
    serializer_class=GameSerializer
    pagination_class = GamePagination

    def get_queryset(self):
        qs=super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(game_name__icontains=query)
        if query:
            qs = qs.filter(conditions)

        return qs

class LoanedGameViewSet(ModelViewSet):
    serializer_class = LoanedGameSerializer
    queryset=LoanedGame.objects.all()

    def get_serializer_class(self):
        method=self.request.method
        if method == "PUT" or method == "POST" or method == "PATCH":
            return LoanedGameCreationSerializer
        else:
            return LoanedGameSerializer

    def get_queryset(self):
        qs=super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(game_name__icontains=query)
        if query:
            qs = qs.filter(conditions)

        return qs