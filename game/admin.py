from django.contrib import admin
from .models import Answer, Lobby
from .models import Question
from .models import UserQuestionHistory
from .models import Result
from .models import Player
from .models import Lobby


admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(UserQuestionHistory)
admin.site.register(Result)
admin.site.register(Player)
admin.site.register(Lobby)
