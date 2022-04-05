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
router.register("review", views.ReviewViewSet)
# router.register("naver_api", views.naver_api)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/naver_api/", views.naver_api),
    # path('send/',MailView.as_view()),

]