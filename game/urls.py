from django.urls import path, include
from rest_framework.routers import DefaultRouter

from game import views

app_name="game"

router=DefaultRouter()
router.register("game",views.GameViewSet)
router.register("loanedgame",views.LoanedGameViewSet)

urlpatterns=[
    path("api/",include(router.urls)),
]
