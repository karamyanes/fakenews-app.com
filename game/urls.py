from django.urls import path, include
from . import api
from rest_framework import routers


router = routers.DefaultRouter()
router.register('question', api.QuestionView)
router.register("lobby_question", api.LobbyQuestionView)

urlpatterns = [
    path('', include(router.urls)),
    path('answer_single/', api.AnswerView.as_view()),
    path('new_game/', api.CreatGame.as_view()),
	#path("add_game_questions/", api.GameQuestion.as_view()),
	path("join_game/", api.JoinGame.as_view() ),
	path("answer_game/", api.MultiPlayerAnswer.as_view() ),
    path("available_game/", api.ListAvailableGames.as_view()),
    path("question_game/", api.QuestionGame.as_view()),
    path('lobby_doc/<game_id>/<question_id>/', api.LobbyQuestionUpdate.as_view(), name='LobbyQuestionUpdate'),
    path('lobby_score/<game_id>/<user_status>/<user_id>/', api.ScoreUpdate.as_view(), name='ScoreUpdate'),
    path('lobby_join/<game_name>/', api.JoinSuccessful.as_view(), name='JoinSuccessful'),
    path('get_hint/<game_id>/<question_id>/', api.GetHint.as_view(), name='GetHint'),
    path('get_score/<game_id>/<user_status>/<user_id>/', api.GetScore.as_view(), name='GetScore'),
    path('get_lobby_join/<game_name>/', api.GetJoinSuccessful.as_view(), name='JoinSuccessful'),
    #path('addgame_questions/', api.AddLobbyQuestions.as_view()),
]
