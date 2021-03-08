from django.db.models import Q
from rest_framework import generics, permissions, response, viewsets,status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Lobby, UserQuestionHistory, Player, Question, Answer, Result , GameQuestions
from .serializers import QuestionListSerializer, AnswerListSerializer, PlayerSerializer, LobbySerializer, GameQuestionSerializer
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
			#Player.objects.get_or_create(user=current_user, game_id=10000)  # game id = 10000 is single player game_id
			game_obj = Lobby.objects.get(pk=10000)
			try:
				obj = Player.objects.get(user=current_user, game_id=game_obj.id)
			except Player.DoesNotExist:
				obj = Player(user=current_user, game_id=game_obj)
				obj.save()
			#update user status
			Player.objects.filter(user=current_user).update(user_status='single_player')
			
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
	serializer_class = GameQuestionSerializer 
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		game_id = request.POST['game_id']
		if game_id == 10000 : #  game id must not equal 10000 (this is game_id = 10000 for single player)
			return Response({
					'Error' : 'you can not add questions for singleplayer',
					'status': status.HTTP_400_BAD_REQUEST
					})
		game = Lobby.objects.get(pk=game_id)
		# we prevent user to add more questions to current game
		#if game :
		#	return Response({
		#			'Error' : 'you can not add new questions for current game',
		#			'status': status.HTTP_400_BAD_REQUEST
		#			})
		# we need to make sure that the player who add the question is questioner 
		current_user = self.request.user
		player_obj = Player.objects.get(game_id=game_id)
		if player_obj.user_status != 'questioner' and player_obj.user != current_user  :
			return Response({
					'Error' : 'this user is not questioner',
					'status': status.HTTP_400_BAD_REQUEST
					})
		data = request.data
		if isinstance(data, list):
			serializer = self.get_serializer(data=request.data, many=True)
			print(data,'pppppppppppppppppppppppppppppppppppppppppppppp')
		else:
			serializer = self.get_serializer(data=request.data)
			print(data,'sssssssssssssssssssssssssssssssssssssssssss')
		serializer.is_valid(raise_exception=True)
		#self.perform_create(serializer)
		serializer.save()
		#headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	
	#def post(self, request, *args, **kwargs):
		#  serializer = LobbySerializer(data=request.data)
	#	game_id = request.POST['game_id']  
	#	question_ids = request.POST['question_ids']
	#	game = Lobby.objects.get(pk=game_id)
	#	game_name = game.game_name
	#	serialized = GameQuestionSerializer(data=request.data, many=True) # many refere to many question that we have it.
	#	if serialized.is_valid():
	#		serialized.save()
		#for question in question_ids: 
			# we need to insert question into GameQuestions model
		#	GameQuestions.objects.create(game_id=game_id, question_id=question)

	#		return Response({
	#				"message" : "questions inserted into %s " % game_name ,
	#				"data" : serialized.data
	#			})


		

#  GET ListGameQuestions (game_id):
#  We need to query on GameQuestions to get all questions related to that game_id
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
