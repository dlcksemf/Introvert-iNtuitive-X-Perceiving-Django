from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from books.models import Books, LoanedBooks, Wishes, Applications, Category, Review
from books.paginations.BookApplicationsPagination import BookApplicationPagination
from books.serializers import BooksSerializer, LoanedBooksSerializer, WishesSerializer, ApplicationsSerializer, \
    LoanedBooksCreationSerializer, CategorySerializer, CategoryCreationSerializer, WishesCreationSerializer, \
    ReviewSerializer


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


class LoanedBooksViewSet(ModelViewSet):
    queryset = LoanedBooks.objects.all()
    pagination_class = BookApplicationPagination

    def get_serializer_class(self):
        method = self.request.method
        if method == "PUT" or method == "POST" or method == "PATCH":
            return LoanedBooksCreationSerializer
        else:
            return LoanedBooksSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(book_name__title__icontains=query) | Q(book_name__writer__icontains=query)
        if query:
            qs = qs.filter(conditions)

        user_id = self.request.query_params.get("user_id", "")
        user_id_conditions = Q(user_id__exact=user_id)
        if user_id:
            qs = qs.filter(user_id_conditions)

        return_state = self.request.query_params.get("state", "")
        return_state_conditions = Q(return_state__exact=return_state)
        if return_state:
            qs = qs.filter(return_state_conditions)

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
    serializer_class = ReviewSerializer

    def get_queryset(self):
        qs=super().get_queryset()

        query = self.request.query_params.get("query", "")
        conditions = Q(name__icontains=query)
        if query:
            qs = qs.filter(conditions)

        return qs