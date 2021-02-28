from django.db.models import Q
from rest_framework import generics, permissions, response, viewsets
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import Lobby, UserQuestionHistory, Player, Question, Answer, Result
from .serializers import QuestionListSerializer, AnswerListSerializer, PlayerListSerializer, LobbySerializer
from rest_framework.response import Response


class QuestionView(viewsets.ModelViewSet):
	"""
	A simple ViewSet for view, edit and delete Transactions.
	"""
	queryset = Question.objects.all()
	serializer_class = QuestionListSerializer
	# permission_classes = [permissions.IsAuthenticated] #this permission we need to be sure that only permited user can use this url


class AnswerView(generics.GenericAPIView):
	"""
	A simple GenericAPIView for view, add game.
	"""
#	queryset = Answer.objects.all()
	serializer_class = AnswerListSerializer
	permission_classes = [permissions.IsAuthenticated] #this permission we need to be sure that only permited user can use this url

	def post(self, request, *args, **kwargs):
		"""
		1- we have to serilaizer the request 
		2- get question correct answer by request.question_id
		"""
		# we have to serilaizer the request
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		# get question correct answer by request.question_id
		question_id = request.POST['questionid']
		obj_question = Question.objects.get(pk=question_id)
		answer = serializer.save()  # save data in db

		 
		current_user = self.request.user
		
		# we will update the is_correct field if 'user answer' is same / correct "question answer"
		if request.POST['answer_text'] == obj_question.correct_answer:
			answer.is_correct = True
			answer.save()  # To save the answer in db

			# insert into player
			Player.objects.get_or_create(user=current_user)

			# update score
			current_player = Player.objects.get(user=current_user)  # user her is refere to the user field in Player model (table)
			new_score = current_player.score + 1  # get the current_score and increase it 
			Player.objects.filter(user=current_user).update( score = new_score )  #  updating the user score with new value

			return Response({
				"answer" : AnswerListSerializer(answer, context=self.get_serializer_context()).data,
				"score"  : new_score,
			})
		else : 
			current_player = Player.objects.get(user=current_user)
			score = current_player.score
			return Response({
				"message" : "your answer is not correct" ,
				"score"  : score,
			})
			
		 		 
class PlayerView(generics.GenericAPIView):
	"""
	A simple GenericAPIView for view, add game.
	"""
	queryset = Player.objects.all()
	serializer_class = PlayerListSerializer
	permission_classes = [permissions.IsAuthenticated]


class GameQuestion(generics.GenericAPIView):
    pass


class JoinGame(generics.GenericAPIView):
	pass


#class LobbyView(generics.GenericAPIView):
	"""
	A simple ViewSet for view, edit and delete Transactions.
	"""
""" 	#queryset = Lobby.objects.all()
	serializer_class = PlayerListSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		current_players = request.POST['current_players']
		num_of_players = request.POST['num_of_players']
		current_user = self.request.user """
		

class CreatGame(generics.GenericAPIView):
	"""
	A simple GenericAPIView for view, add game.
	"""
	serializer_class = LobbySerializer
	permission_classes = [permissions.IsAuthenticated]
	
	#create game for first time
	def post(self, request, *args, **kwargs):
		current_user = self.request.user
		print(current_user)
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		game = serializer.save()
		print(game.id)
		new_player = game.current_players + 1
		#game.update( current_player = new_player)
		game.current_players = new_player
		game.save()
		game_filter = Lobby.objects.get(pk=game.id)
		creater = Player.objects.create(user=current_user, game_id = game.id, user_status = 'questioner')

		return Response({
				"message" : "Succsesfully created game" ,
				"game"    : game ,
				'newPlayer' : creater
			})


