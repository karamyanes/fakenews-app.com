from django.urls import path, include
from . import api
# from .api import TransactionListAPI
from rest_framework import routers

router = routers.DefaultRouter()
router.register('question', api.QuestionView)
router.register('player',api.PlayerView)



urlpatterns = [
    path('', include(router.urls)),
    path('answer/', api.AnswerView.as_view()),
   #  path('question/',include(router.urls)),
	# path("transaction/list/", TransactionListAPI.as_view()),
]
