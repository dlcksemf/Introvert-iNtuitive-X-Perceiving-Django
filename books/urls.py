from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books import views

app_name = "books"

router = DefaultRouter()
router.register("books", views.BooksViewSet)
router.register("loanedbooks", views.LoanedBooksViewSet)
router.register("newloanedbooks", views.LoanedBooksCreationViewSet)
router.register("wishes", views.WishesViewSet)
router.register("applications", views.ApplicationsViewSet)

urlpatterns = [
    path("api/",include(router.urls)),

]