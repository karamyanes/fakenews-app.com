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
	permission_classes = [permissions.IsAuthenticated] #this permission we need to be sure that only permited user can use this url


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
		#we have to serilaizer the request
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		#get question correct answer by request.question_id
		question_id = request.POST['questionid']
		obj_question = Question.objects.get(pk=question_id)
		#obj_question.correct_answer
		#print(obj_question)
		#if request.POST['answer_text'] == request.POST['correct_answer']
		if request.POST['answer_text'] == obj_question.correct_answer:
			serializer.is_correct = True
		else :
			serializer.is_correct = False
		answer = serializer.save()
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
