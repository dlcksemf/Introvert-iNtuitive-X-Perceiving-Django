from django.db.models import Q
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from game.models import Game, LoanedGame
from game.serializers import GameSerializer


class GameViewSet(ModelViewSet):
    queryset=Game.objects.all()
    serializerr_class=GameSerializer

    def get_query(self):
        qs=super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(game_name__icontains=query)
        if query:
            qs = qs.filter(conditions)

class LoanedGameViewSet(ModelViewSet):
    queryset=LoanedGame.objects.all()

    # def get_serializer_class(self):
    #     method=self.request.method
    #     if method == "PUT" or method == "POST" or method == "PATCH":
    #         return LoanedGameCreationSerializer
    #     else:
    #         return LoanedGameSerializer

    def get_queryset(self):
        qs=super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(game_name__title__icontains=query)
        if query:
            qs = qs.filter(conditions)