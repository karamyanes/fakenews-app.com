from .models import Lobby, Player, Question, Answer, LobbyQuestion
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


class LobbySerializer(serializers.ModelSerializer):
	class Meta:
		model = Lobby
		fields = "__all__"


class LobbyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LobbyQuestion
        fields = "__all__"
