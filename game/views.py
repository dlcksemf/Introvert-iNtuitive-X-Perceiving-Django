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

import smtplib
from email.mime.text import MIMEText
import requests
from django.conf import settings
from rest_framework.response import Response
from datetime import datetime, timedelta

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

    def send_email(smtp_info, msg):
        EMAIL_HOST_PASSWORD = getattr(settings, "EMAIL_HOST_PASSWORD", "EMAIL_HOST_PASSWORD")
        smtp_info = dict({"smtp_server": "smtp.naver.com",  # SMTP 서버 주소
                          "smtp_user_id": "euclidsoft_books@naver.com",
                          "smtp_user_pw": EMAIL_HOST_PASSWORD,
                          "smtp_port": 587})  # SMTP 서버 포트

        with smtplib.SMTP(smtp_info["smtp_server"], smtp_info["smtp_port"]) as server:
            # TLS 보안 연결
            server.starttls()
            # 로그인
            server.login(smtp_info["smtp_user_id"], smtp_info["smtp_user_pw"])

            response = server.sendmail(msg['from'], msg['to'], msg.as_string())

            if not response:
                print('이메일을 성공적으로 보냈습니다.')
            else:
                print(response)

    def create(self, request, *args, **kwargs):
        if request.method == "POST":
            username = request.user.username
            email = request.user.email
            game = Game.objects.get(game_num=request.data["game_name"])
            gamename = game.game_name
            returntime = request.data["return_due_time"]
            returnduetime = returntime[2:16].replace('T', ' ')
            date_time_returnduetime = datetime.strptime(returnduetime, '%y-%m-%d %H:%M')
            returntime_kr = date_time_returnduetime + timedelta(hours=9)
            title = "다독다독 유클리드 소프트 게임 대출 안내 메세지입니다"
            content = f"""
{username}님 안녕하세요!
{username}님이 빌린 게임은 {gamename}입니다.
{returntime_kr}까지 반납해야 합니다.
            """
            sender = "euclidsoft_books@naver.com"
            receiver = f'{email}'
            # # 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
            msg = MIMEText(_text=content, _charset="utf-8")  # 메일 내용

            msg['Subject'] = title  # 메일 제목
            msg['From'] = sender  # 송신자
            msg['To'] = receiver  # 수신자

            self.send_email(msg)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

        return Response(serializer.data)

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

        game_num = self.request.query_params.get("game_num", "")
        game_num_conditions = Q(game_name__exact=game_num)
        if game_num:
            qs = qs.filter(game_num_conditions)

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