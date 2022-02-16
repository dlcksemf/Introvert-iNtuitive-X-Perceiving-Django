from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books import views

app_name = "books"

router = DefaultRouter()
router.register("books", views.BooksViewSet)
router.register("loanedbooks", views.LoanedBooksViewSet)
router.register("wishes", views.WishesViewSet)
router.register("applications", views.ApplicationsViewSet)
router.register("category", views.CategoryViewSet)


urlpatterns = [
    path("api/",include(router.urls)),

]