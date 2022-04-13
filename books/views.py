from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.serializers import UserSerializer
from books.models import Books, LoanedBooks, Wishes, Applications, Category, Review
from books.paginations.BookApplicationsPagination import BookApplicationPagination
from books.serializers import BooksSerializer, LoanedBooksSerializer, WishesSerializer, ApplicationsSerializer, \
    LoanedBooksCreationSerializer, CategorySerializer, CategoryCreationSerializer, WishesCreationSerializer, \
    ReviewSerializer, ReviewCreationSerializer, UserListingField, ApplicationsCreationSerializer
import requests
from django.conf import settings
from django.shortcuts import redirect, render

import smtplib
from email.mime.text import MIMEText



class BooksViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    pagination_class = BookApplicationPagination

    #
    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAdminUser()]

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(title__icontains=query) | Q(writer__icontains=query)
        if query:
            qs = qs.filter(conditions)

        state = self.request.query_params.get("state", "")
        state_conditions = Q(state__exact=state)
        if state:
            qs = qs.filter(state_conditions)

        category = self.request.query_params.get("category", "")
        category_conditions = Q(category__exact=category)
        if category:
            qs = qs.filter(category_conditions)

        return qs


from django.conf import settings

class LoanedBooksViewSet(ModelViewSet):
    queryset = LoanedBooks.objects.all()
    pagination_class = BookApplicationPagination


    def get_serializer_class(self):
        method = self.request.method
        if method == "PUT" or method == "POST" or method == "PATCH":
            return LoanedBooksCreationSerializer
        else:
            return LoanedBooksSerializer


    def send_email(smtp_info, msg):
        EMAIL_HOST_PASSWORD=getattr(settings,"EMAIL_HOST_PASSWORD","EMAIL_HOST_PASSWORD")
        smtp_info = dict({"smtp_server": "smtp.naver.com",  # SMTP 서버 주소
                          "smtp_user_id": "jwheein950417@naver.com",
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
        if request.method=="POST":

            username =request.user.username
            email=request.user.email
            # loanedmodal 46번째 줄에서 data로 받아온 정보이기 때문
            # 근데 아래는 pk값을 받는거기 때문에 objects.get으로 받음
            book = Books.objects.get(book_num=request.data["book_name"])
            bookname = book.title
            returndate=request.data["return_due_date"]
            title = "다독다독 유클리드 북스 도서 대출 안내 메일"
            content = f"""
{username}님 안녕하세요! 다독다독 유클리드 북스입니다.
{username}님이 대출하신 {bookname} 도서는 {returndate}까지 반납해주셔야 함을 안내드립니다.

반납하러 가기 -> www.kwondjango.com
            """
            sender = "jwheein950417@naver.com"
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

    def update(self, request, *args, **kwargs):
        if request.method == "PATCH":
            kwargs['partial'] = True
            if request.data["return_state"] == "E":
                username = request.user.username
                email = request.user.email
                instance = self.get_object()
                book = instance.book_name
                bookname = book.title
                returndate = request.data["return_due_date"]
                title = "다독다독 유클리드 북스 도서 연장 안내 메일"
                content = f"""
    {username}님 안녕하세요! 다독다독 유클리드 북스입니다.
    {username}님이 대출하신 {bookname} 도서는 연장 신청이 되어 {returndate}까지 반납해주셔야 함을 안내드립니다.
    
    반납하러 가기 -> www.kwondjango.com
                           """
                sender = "jwheein950417@naver.com"
                receiver = f'{email}'
                # # 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
                msg = MIMEText(_text=content, _charset="utf-8")  # 메일 내용

                msg['Subject'] = title  # 메일 제목
                msg['From'] = sender  # 송신자
                msg['To'] = receiver  # 수신자

                self.send_email(msg)

            return super().update(request, *args, **kwargs)



    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(book_name__title__icontains=query) | Q(user_id__username__icontains=query)
        if query:
            qs = qs.filter(conditions)

        user_id = self.request.query_params.get("user_id", "")
        user_id_conditions = Q(user_id__exact=user_id)
        if user_id:
            qs = qs.filter(user_id_conditions)

        return_state = self.request.query_params.get("state", "")
        return_state_conditions = Q(return_state__exact=return_state)
        if return_state:
            if return_state == "R":
                qs = qs.filter(return_state_conditions)
            else:
                qs = qs.exclude(return_state__exact="R")

        return qs


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAdminUser()]

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT' or method == 'POST':
            return CategoryCreationSerializer
        else:
            return CategorySerializer


class WishesViewSet(ModelViewSet):
    queryset = Wishes.objects.all()
    pagination_class = BookApplicationPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT' or method == 'POST':
            return WishesCreationSerializer
        else:
            return WishesSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(book_name__title__icontains=query) | Q(book_name__writer__icontains=query)
        if query:
            qs = qs.filter(conditions)

        state = self.request.query_params.get("state", "")
        state_conditions = Q(book_name__state__exact=state)
        if state:
            qs = qs.filter(state_conditions)

        user_id = self.request.query_params.get("user_id", "")
        user_id_conditions = Q(user_id__exact=user_id)
        if user_id:
            qs = qs.filter(user_id_conditions)

        book_num = self.request.query_params.get("book", "")
        book_conditions = Q(book_name__exact=book_num)
        if book_num:
            qs = qs.filter(book_conditions)

        return qs


class ApplicationsViewSet(ModelViewSet):
    queryset = Applications.objects.all()
    serializer_class = ApplicationsSerializer
    pagination_class = BookApplicationPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == "PUT" or method == "POST" or method == "PATCH":
            return ApplicationsCreationSerializer
        else:
            return ApplicationsSerializer

    def send_email(smtp_info, msg):
        EMAIL_HOST_PASSWORD = getattr(settings, "EMAIL_HOST_PASSWORD", "EMAIL_HOST_PASSWORD")
        smtp_info = dict({"smtp_server": "smtp.naver.com",  # SMTP 서버 주소
                          "smtp_user_id": "jwheein950417@naver.com",
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

    def update(self, request, *args, **kwargs):
        if request.method == "PATCH":
            kwargs['partial'] = True
            if request.data["state"] == "O":
                # partial = kwargs.pop('partial', False)
                instance = self.get_object()
                # serializer = self.get_serializer(instance, data=request.data, partial=partial)
                # serializer.is_valid(raise_exception=True)
                # self.perform_update(serializer)
                # email = instance.email
                username = instance.user_id.username
                email = instance.user_id.email
                bookname = instance.title
                mailtitle = "다독다독 유클리드 북스 도서 신청 안내 메일"
                content = f"""
{username}님 안녕하세요! 다독다독 유클리드 북스입니다.
{username}님이 주문하신 {bookname} 도서가 입고되었습니다. 대출해보세요!

확인하러 가기 -> www.kwondjango.com
                           """
                sender = "jwheein950417@naver.com"
                receiver = f'{email}'
                # # 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
                msg = MIMEText(_text=content, _charset="utf-8")  # 메일 내용

                msg['Subject'] = mailtitle  # 메일 제목
                msg['From'] = sender  # 송신자
                msg['To'] = receiver  # 수신자

                self.send_email(msg)

            if request.data["state"] == "D":
                # partial = kwargs.pop('partial', False)
                instance = self.get_object()
                # serializer = self.get_serializer(instance, data=request.data, partial=partial)
                # serializer.is_valid(raise_exception=True)
                # self.perform_update(serializer)
                # email = instance.email
                username = instance.user_id.username
                email = instance.user_id.email
                bookname = instance.title
                mailtitle = "다독다독 유클리드 북스 도서 신청 안내 메일"
                content = f"""
{username}님 안녕하세요! 다독다독 유클리드 북스입니다.
{username}님이 주문하신 {bookname} 도서가 반려되었음을 안내해드립니다.

확인하러 가기 -> www.kwondjango.com

                                      """
                sender = "jwheein950417@naver.com"
                receiver = f'{email}'
                # # 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 체계인 UTF-8을 명시해줍니다.
                msg = MIMEText(_text=content, _charset="utf-8")  # 메일 내용

                msg['Subject'] = mailtitle  # 메일 제목
                msg['From'] = sender  # 송신자
                msg['To'] = receiver  # 수신자

                self.send_email(msg)

            return super().update(request, *args, **kwargs)


    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(title__icontains=query) | Q(writer__icontains=query)
        if query:
            qs = qs.filter(conditions)

        state = self.request.query_params.get("state", "")
        state_conditions = Q(state__exact=state)
        if state:
            qs = qs.filter(state_conditions)

        user_id = self.request.query_params.get("user_id", "")
        user_id_conditions = Q(user_id__exact=user_id)
        if user_id:
            qs = qs.filter(user_id_conditions)

        return qs

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    pagination_class = BookApplicationPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT' or method == 'POST':
            return ReviewCreationSerializer
        else:
            return ReviewSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(book_name__title__icontains=query) | Q(user_id__username__icontains=query)
        if query:
            qs = qs.filter(conditions)

        book_num = self.request.query_params.get("book_num", "")
        book_num_conditions = Q(book_name__exact=book_num)
        if book_num:
            qs = qs.filter(book_num_conditions)

        return qs

@api_view()
def naver_api(request):
    headers ={'X-Naver-Client-Id': settings.NAVER_CLIENT_ID,
             'X-Naver-Client-Secret': settings.NAVER_CLIENT_SECRET}


    query = request.query_params.get("query", "")
    params = {"query":query, "d_isbn": str(query)}
    response = requests.get("https://openapi.naver.com/v1/search/book_adv.json", headers=headers, params=params)
    qs = response.json()
    print(qs)
    print(type(qs))
    return Response(qs)


# Prepare a map of common locations to timezone choices you wish to offer.
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



