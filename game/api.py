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
	# permission_classes = [permissions.IsAuthenticated] #this permission we need to be sure that only permited user can use this url

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
<<<<<<< HEAD
		obj_question = Question.objects.get(pk=question_id)
		#print(serializer)
		if request.POST['answer_text'] == obj_question.correct_answer:
			print('check if condition')
			serializer.is_correct = True
		#else :
		#	print('check ELSE condition')
		#	serializer.is_correct = 0
		answer = serializer.save()
=======
		obj_questions = Question.objects.get(pk=question_id)
		answer = serializer.save()  # save data in db

		# we will update the is_correct field if 'user answer' is same / correct "question answer"
		if request.POST['answer_text'] == obj_questions.correct_answer:
			answer.is_correct = True
			answer.save()  # To save the answer in db

>>>>>>> 3d8c78952076e6a97dd8cfde025e799aadde40e9
		return Response({
			"answer" : AnswerListSerializer(answer, context=self.get_serializer_context()).data,
		})
			
		 		 
class PlayerView(viewsets.ModelViewSet):
	"""
	A simple ViewSet for view, edit and delete Transactions.
	"""
	queryset = Player.objects.all()
	serializer_class = PlayerListSerializer
	permission_classes = [permissions.IsAuthenticated]
