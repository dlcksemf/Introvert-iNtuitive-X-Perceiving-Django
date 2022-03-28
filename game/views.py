from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet

from game.models import Game, LoanedGame, GameReview
from game.serializers import GameSerializer, LoanedGameSerializer, LoanedGameCreationSerializer, \
    GameReviewCreationSerializer, GameReviewSerializer
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

        game_state = self.request.query_params.get("game_state", "")
        game_state_conditions = Q(game_state__exact=game_state)
        if game_state:
            qs = qs.filter(game_state_conditions)

        return qs

class LoanedGameViewSet(ModelViewSet):
    serializer_class = LoanedGameSerializer
    queryset=LoanedGame.objects.all()
    pagination_class = GamePagination

    def get_serializer_class(self):
        method=self.request.method
        if method == "PUT" or method == "POST" or method == "PATCH":
            return LoanedGameCreationSerializer
        else:
            return LoanedGameSerializer

    def get_queryset(self):
        qs=super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(game_name__game_name__icontains=query)
        if query:
            qs = qs.filter(conditions)

        user_id = self.request.query_params.get("user_id", "")
        user_id_conditions = Q(user_id__exact=user_id)
        if user_id:
            qs = qs.filter(user_id_conditions)

        return_state = self.request.query_params.get("return_state", "")
        return_state_conditions = Q(return_state__exact=return_state)
        if return_state:
            qs = qs.filter(return_state_conditions)

        return qs

class GameReviewViewSet(ModelViewSet):
    queryset = GameReview.objects.all()
    pagination_class = GamePagination

    def get_serializer_class(self):
        method = self.request.method
        if method == "PUT" or method == "POST":
            return GameReviewCreationSerializer
        else:
            return GameReviewSerializer


    def get_queryset(self):
        qs=super().get_queryset()

        query=self.request.query_params.get("query","")
        conditions=Q(game_name__game_name__icontains=query)| Q(user_id__username__icontains=query)
        if query:
            qs = qs.filter(conditions)

        return  qs

# common_timezones = {
#     'Seoul': 'Asia/Seoul',
# }
#
# def set_timezone(request):
#     if request.method == 'POST':
#         request.session['django_timezone'] = request.POST['timezone']
#         return redirect('/')
#     else:
#         return render(request, 'template.html', {'timezones': common_timezones})