from django.db.models import Q
from rest_framework import generics, permissions, response, viewsets,status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Lobby, UserQuestionHistory, Player, Question, Answer, Result
from .serializers import QuestionListSerializer, AnswerListSerializer, PlayerSerializer, LobbySerializer
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
			#update user status
			Player.objects.filter(user=current_user).update(user_status = 'single_player')
			# we need to create game_id and update Player table with game_id ; when he press single player so he should get new player and new game_id (Lobby)
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
	serializer_class = PlayerSerializer
	permission_classes = [permissions.IsAuthenticated]


class GameQuestion(generics.GenericAPIView):
    pass


class JoinGame(generics.GenericAPIView):
	serializer_class = PlayerSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		"""
		the palyer join the game so he need 1- game id -2- we have to know number of player 
		i have to make sure that there is a place for new player
		"""
		game_id = request.POST['game_id']  
		game_obj = Lobby.objects.get(pk=game_id)  # we make query on lobby table by primery key =  game_id
		num_of_players = game_obj.num_of_players  # we bring from game_obj num_of_players and current_players
		current_players = game_obj.current_players 
		player_obj = Player.objects.get(game_id=game_id)
			# we check if current_players smaller than num_of_players and we not alowed the same user to join the same game again
		if current_players < num_of_players and player_obj.user.id != int(request.POST['user']) and player_obj.user_status != request.POST['user_status'] :
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			#current_user = self.request.user
			serializer.save()
			new_count_player = current_players + 1
			Lobby.objects.filter(pk=game_id).update( current_players = new_count_player)
			return Response({
				'message' : ' sucsefull join the game',
				'player' : serializer.data,
			})
		else:
			return Response({'message' : 'no places game is full or you allready joined the game',})
			
		
class CreatGame(APIView):
	"""
	A simple GenericAPIView for view, add game.
	"""
	permission_classes = [permissions.IsAuthenticated]
	
	#create game for first time
	def post(self, request, format=None):
	
		serializer = LobbySerializer(data=request.data)
		if serializer.is_valid():
			game_obj = serializer.save()
			current_user = self.request.user
			try:
				player_obj = Player.objects.create(user=current_user, game_id=game_obj, user_status='questioner')
				# import json
				# from django.forms.models import model_to_dict
				# play = json.dumps(model_to_dict(player_obj))

				return Response({
					"message" : "Game successfully created" ,
					"game" : serializer.data ,
					"player_game" : player_obj.id,
					"status": status.HTTP_201_CREATED
					})
			except:
				# Roll-back :: delete the record created by Lobby serializer
				loby_obj = Lobby.objects.get(pk=game_obj.id)
				loby_obj.delete()
				return Response({
					'Error' : 'game not created',
					'status': status.HTTP_400_BAD_REQUEST
					})

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
