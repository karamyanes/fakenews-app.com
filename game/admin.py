from django.contrib import admin
from .models import Answer, Lobby, Question, Player, LobbyQuestion


admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Player)
admin.site.register(Lobby)
admin.site.register(LobbyQuestion)
