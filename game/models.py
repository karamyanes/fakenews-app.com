from django.db import models
from django.contrib.auth.models import User


class Lobby(models.Model):
    game_name = models.CharField(max_length=20)
    num_of_players = models.IntegerField(default=2)
    current_players = models.IntegerField(default=0)



class Question(models.Model):
    STATUS=(
        ('true','true'),
        ('barely-true','barely-true'),
        ('false','false'),
        ('mostly-true','mostly-true'),
        ('pants-fire','pants-fire'),
    )
    question_text = models.CharField(max_length=2000)
    correct_answer = models.CharField(max_length=100,choices=STATUS)
    game_id = models.ForeignKey(Lobby, default=0, on_delete=models.CASCADE, verbose_name = "related to Lobby")# we cannot make default = 0
    # because he reason maybe is that you have tried to add a foreign key to a model which uses AutoField as its primary key
    
    
    def __str__(self):
        return self.question_text


class Answer(models.Model):
    STATUS=(
        ('true','true'),
        ('barely-true','barely-true'),
        ('false','false'),
        ('mostly-true','mostly-true'),
        ('pants-fire','pants-fire'),
    )
    questionid=models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name = "related to Question")
    answer_text= models.CharField(max_length=256,choices=STATUS)
    is_correct=models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


# class player is extended class from class User so it is extend user database
class Player(models.Model):
    Status=(
        ('questioner', 'questioner'),
        ('respondent', 'respondent'),
        ('single_player','single_player'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, null=True, blank=True)
    game_id = models.ForeignKey(Lobby, default=0, on_delete=models.CASCADE, verbose_name = "related to Lobby")
    user_status= models.CharField(max_length=256,choices=Status)

    def str(self):
        return self.user.username
    
class UserQuestionHistory(models.Model):
    questioner_id= models.ForeignKey(Player, on_delete=models.CASCADE, related_name = "questioner")
    respoender_id= models.ForeignKey(Player, on_delete=models.CASCADE, related_name = "respoender")


class Result(models.Model):
    answer_id= models.ForeignKey(Answer, on_delete=models.CASCADE, related_name = "Answer") 
    question_id= models.ForeignKey(Question, on_delete=models.CASCADE, related_name = "spørsmål")
    questioner_id= models.ForeignKey(Player, on_delete=models.CASCADE, related_name = "Player_1")
    respondent_id=models.ForeignKey(Player, on_delete=models.CASCADE, related_name = "Player_2")
