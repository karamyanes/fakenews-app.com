from django.urls import path, include
from . import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register('question', api.QuestionView)


urlpatterns = [
    path('', include(router.urls)),
    path('answer_single/', api.AnswerView.as_view()),
    path('new_game/', api.CreatGame.as_view()),
	#path("add_game_questions/", api.GameQuestion.as_view()),
	#path("join_game/", ),
	#path("game_answer/", api.AnswerView.as_view() ),
   #  path('question/',include(router.urls)),
	# path("transaction/list/", TransactionListAPI.as_view()),
]
