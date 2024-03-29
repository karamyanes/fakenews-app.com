from django.db import models
from django.db.models import Q
from django.db.models import F
from rest_framework import generics, permissions, response, viewsets,status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Lobby, LobbyQuestion, Player, Question, Answer
from .serializers import QuestionListSerializer, AnswerListSerializer, PlayerSerializer, LobbySerializer, LobbyQuestionSerializer
from rest_framework.response import Response
import json
from django.core import serializers
from rest_framework.throttling import UserRateThrottle
import datetime



class QuestionView(viewsets.ModelViewSet):
	"""
	A simple ViewSet for view, edit and delete Transactions.
	"""
	queryset = Question.objects.all()
	serializer_class = QuestionListSerializer
	#permission_classes = [permissions.IsAuthenticated] #this permission we need to be sure that only permited user can use this url


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
		serializer.is_valid(raise_exception=True) #  You need to call is_valid during deserialization process before write data to DB. is_valid perform validation of input data and confirm that this data contain all required fields and all fields have correct types.
		#  raise_exception=True, this exception and return 400 response with the provided errors in form of list or dictionary.
		# get question correct answer by request.question_id
		question_id = request.POST['questionid']
		obj_question = Question.objects.get(pk=question_id)
		answer = serializer.save()  # save data in db,insert the answer in database

		 
		current_user = self.request.user
		game_obj = Lobby.objects.get(pk=1)
		# we will update the is_correct field if 'user answer' is same / correct "question answer"
		if request.POST['answer_text'] == obj_question.correct_answer:
			answer.is_correct = True 
			answer.save()  # To update / set  is correct field with True in database
			# insert into player
			#Player.objects.get_or_create(user=current_user, game_id=1)  # game id = 1 is single player game_id
			#game_obj = Lobby.objects.get(pk=1)
			try:
				obj = Player.objects.get(user=current_user, game_id=game_obj.id)
			except Player.DoesNotExist:
				obj = Player(user=current_user, game_id=game_obj)
				obj.save()
			#update user status
			Player.objects.filter(user=current_user).update(user_status='single_player')
			
			# update score
			new_score = obj.score + 1  # get the current_score and increase it 
			Player.objects.filter(user=current_user, game_id=game_obj).update( score = new_score )  #  updating the user score with new value

			return Response({
				"answer" : AnswerListSerializer(answer, context=self.get_serializer_context()).data,
				"score"  : new_score,
			})
		else : 
			#current_player = Player.objects.get(user=current_user,game_id=game_obj.id)
			#score = current_player.score
			return Response({
				"message" : "your answer is not correct" ,
			#	"score"  : score,
			})
			
		 		 
class PlayerView(generics.GenericAPIView):
	"""
	A simple GenericAPIView for view, add game.
	"""
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer
	permission_classes = [permissions.IsAuthenticated]


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
		current_user = self.request.user
		#player_obj = Player.objects.get(game_id=game_id,user=current_user)
		# we check if current_players smaller than num_of_players and we not alowed the same user to join the same game again
		#player_obj.user_status != request.POST['user_status'] :
		if Player.objects.filter(game_id=game_id,user=current_user).exists():
			player_obj = Player.objects.get(game_id=game_id,user=current_user)
			if player_obj.user.id == current_user.id:  #or player_obj.user_status == 'respondent' : 
				return Response({
					'message' : ' user already joined the game',
				})
		#we need to remove user status and user id in postman 
		if current_players < num_of_players:
			request.data._mutable = True # to enable updating data
			request.data['user_status'] = 'respondent'
			request.data['user'] = current_user.id
			request.data._mutable = False # to disable updating data (im_mutable) we do imutable and immutable because database donot accept mutable data
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)

			if  LobbyQuestion.objects.filter(game_id=game_id).exists():
				questions_set = set()
				for e in LobbyQuestion.objects.filter(game_id=game_id).select_related('question_id'):
					questions_set.add(e.question_id)
				
				questions_set_json = serializers.serialize("json", questions_set)
				questions_set_result = json.loads(questions_set_json)
				print(questions_set_result)
				# finally saving serializer after making sure that game has questions 
				# ... also after making sure serializer is valid 
				serializer.save()
				new_count_player = current_players + 1
				Lobby.objects.filter(pk=game_id).update( current_players = new_count_player)

				return Response({
						'message' : 'sucsefull join the game',
						'player' : serializer.data,
						'question_set' : questions_set_result, 
					})
			else: 
				#  there are no questions in the game so user can not join the game 
				return Response({
					'restult' : 'You can not join the game because there are no questions',
					})	
		else:
			#  the game is full so user can not join
			return Response({'message' : 'no places game is full or you allready joined the game',})
			
		
class CreatGame(APIView):
	"""
	A simple GenericAPIView for view, add game.
	"""
	permission_classes = [permissions.IsAuthenticated]
	
	#create game for first time
	def post(self, request, format=None):
	
		serializer = LobbySerializer(data=request.data)  # returns the parsed content of the request body
		if serializer.is_valid():
			game_obj = serializer.save()
			game_obj.current_players = 1 # we update current_players with 1 because questioner is first player. and in database the default value for current_player is 0
			game_obj.save()
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

class MultiPlayerAnswer(generics.GenericAPIView):
	serializer_class = AnswerListSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)  
		serializer.is_valid(raise_exception=True)
		question_id = request.POST['questionid']
		game_id = request.POST['game_id']
		current_user = self.request.user
		player_obj = Player.objects.get(game_id=game_id, user=current_user)
		obj_question = Question.objects.get(pk=question_id)
		lobby_obj = Lobby.objects.get(pk=game_id)
		# player_obj.user_status == 'respondent' and player_obj.user != current_user and request.POST['answer_text'] == obj_question.correct_answer:
		if not lobby_obj :
			return Response({
				"message" : "Game not correct" ,
			})
		if  player_obj.user_status != 'respondent':
			return Response({
				"message" : "Wrong user" ,
			})
		if request.POST['answer_text'] == obj_question.correct_answer:
			answer = serializer.save()
			answer.is_correct = True
			answer.save()				
			return Response({
				"message" : "your answer is correct",
				"answer" : AnswerListSerializer(answer, context=self.get_serializer_context()).data,
			})
		if request.POST['answer_text'] != obj_question.correct_answer:
			answer = serializer.save()
			answer.is_correct = False
			answer.save()	
			return Response({
				"message" : "your answer is wrong" ,
			})
		else : 
			return Response({
				"message" : "unknown error please try again" ,
			})


class ListAvailableGames(generics.ListAPIView):
	serializer_class = LobbySerializer

	def get(self, request):
		#time_diff = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=1)

		time_diff = datetime.datetime.now() - datetime.timedelta(hours=1)	
		queryset = Lobby.objects.filter(
			current_players__lt=F('num_of_players'), 
			created_at__gt=time_diff
			) # lt = lessthan , gt=greater than
		tmpJson = serializers.serialize("json", queryset) # we convert queryset to serializable Json  Object
		result = json.loads(tmpJson)  # we load tmJson Object

		if queryset:
			return Response({
				"message" : "Games listed successfully",
				"games" : result,
				"status": status.HTTP_201_CREATED
			})


class QuestionGame(generics.GenericAPIView):
	serializer_class = QuestionListSerializer
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, *args, **kwargs):
		#game_id = request.POST['game_id']
		# we need to updat data with game_id
		serializer = self.get_serializer(data=request.data)  
		serializer.is_valid(raise_exception=True)
		serializer.save()
		#question =serializer.save()
		#print(question)
		return Response({
                "message" : "question added successfully",
                "question" : serializer.data,
                "status": status.HTTP_201_CREATED
            })
		#question_id = request.POST['questionid']
		#correct_answer = request.POST['correct_answer']


class LobbyQuestionView(viewsets.ModelViewSet):
    """
    A simple ViewSet for view, edit and delete LobbyQuestions.
    """
    queryset = LobbyQuestion.objects.all()
    serializer_class = LobbyQuestionSerializer
    #permission_classes = [permissions.IsAuthenticated]


class LobbyQuestionUpdate(APIView):
	queryset = LobbyQuestion.objects.all()
	serializer_class = LobbyQuestionSerializer

	def put(self, request, *args, **kwargs):
		game_id = self.kwargs['game_id']
		question_id = self.kwargs['question_id']
		question_object = LobbyQuestion.objects.get(question_id=question_id,game_id=game_id)
		question_object.doc_hint = request.POST['doc_hint']
		question_object.save()
		return Response({
                "message" : "doc updated sucsessfuly",
                "status": status.HTTP_201_CREATED,
				"doc_hint": request.POST['doc_hint'],
            })
			

class ScoreUpdate(APIView):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer

	def put(self, request, *args, **kwargs):
		game_id = self.kwargs['game_id']
		user_status= self.kwargs['user_status']
		user_id = self.kwargs['user_id']
		score_object = Player.objects.get(game_id=game_id, user_status=user_status, pk=user_id)
		score_object.score = request.POST['score']
		score_object.save()
		return Response({
			"message" : "score updated sucsessfuly",
                "status": status.HTTP_201_CREATED,
				"score": request.POST['score'],
		})


class GetHint(APIView):
	queryset = LobbyQuestion.objects.all()
	serializer_class = LobbyQuestionSerializer

	def get(self, request,*args, **kwargs ):
		game_id = self.kwargs['game_id']
		question_id = self.kwargs['question_id']
		question_object = LobbyQuestion.objects.get(question_id=question_id,game_id=game_id)
		return Response({
				"doc_hint": question_object.doc_hint,
            })


class GetScore(APIView):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer

	def get(self, request,*args, **kwargs ):
		game_id = self.kwargs['game_id']
		user_status = self.kwargs['user_status']
		user_id = self.kwargs['user_id']
		
		score_object = Player.objects.get(user_status=user_status, game_id=game_id, pk=user_id)
		return Response({
				"score": score_object.score,
            })
