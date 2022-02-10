from django.db.models import Q
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from books.models import Books, LoanedBooks, Wishes, Applications
from books.serializers import BooksSerializer, LoanedBooksSerializer, WishesSerializer, ApplicationsSerializer


class BooksViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(title__icontains=query) | Q(writer__icontains=query)
        if query:
            qs = qs.filter(conditions)

        return qs

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        qs= super().get_queryset()

        query=self.request.query_params.get("query","")
        if query:
            qs=qs.filter(title__icontains=query)

        return qs


class LoanedBooksViewSet(ModelViewSet):
    queryset = LoanedBooks.objects.all()
    serializer_class = LoanedBooksSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class WishesViewSet(ModelViewSet):
    queryset = Wishes.objects.all()
    serializer_class = WishesSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ApplicationsViewSet(ModelViewSet):
    queryset = Applications.objects.all()
    serializer_class = ApplicationsSerializer

    def perform_create(self, serializer):
        serializer.save(email=self.request.user)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
