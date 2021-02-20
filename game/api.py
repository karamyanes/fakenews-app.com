from django.db.models import Q
from rest_framework import generics, permissions, response, viewsets
from .models import UserQuestionHistory
from .models import Player
from .models import Question
from .models import Answer
from .models import Result
from .serializers import QuestionListSerializer
from .serializers import AnswerListSerializer
from .serializers import PlayerListSerializer
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
	A simple ViewSet for view, edit and delete Transactions.
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
		print(question_id)
		obj_question = Question.objects.get(pk=question_id)
		print(obj_question)
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
	A simple ViewSet for view, edit and delete Transactions.
	"""
	queryset = Player.objects.all()
	serializer_class = PlayerListSerializer
	permission_classes = [permissions.IsAuthenticated]
