from .models import Lobby, UserQuestionHistory , Player, Question, Answer, Result
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = "__all__"


class QuestionListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = "__all__"


class AnswerListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = "__all__"


class ResultListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Result
		fields = "__all__"


class UserQuestionHistoryListSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserQuestionHistory
		fields = "__all__"


class LobbySerializer(serializers.ModelSerializer):
	class Meta:
		model = Lobby
		fields = "__all__"
		