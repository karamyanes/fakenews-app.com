# Generated by Django 3.1.4 on 2021-04-11 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=20)),
                ('num_of_players', models.IntegerField(default=2)),
                ('current_players', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.JSONField()),
                ('correct_answer', models.CharField(choices=[('true', 'true'), ('barely-true', 'barely-true'), ('false', 'false'), ('mostly-true', 'mostly-true'), ('pants-fire', 'pants-fire'), ('half-true', 'half-true')], max_length=100)),
                ('url', models.CharField(max_length=2000, null=True)),
                ('stated_in', models.CharField(max_length=500, null=True)),
                ('speaker', models.CharField(max_length=100, null=True)),
                ('factchecker', models.CharField(max_length=50, null=True)),
                ('published', models.DateField(null=True)),
                ('date_stated', models.DateField(null=True)),
                ('topic', models.TextField(null=True)),
                ('sources', models.JSONField(default=list)),
                ('doc', models.JSONField()),
                ('summary', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, default=0, null=True)),
                ('user_status', models.CharField(choices=[('questioner', 'questioner'), ('respondent', 'respondent'), ('single_player', 'single_player')], max_length=256)),
                ('game_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='game.lobby', verbose_name='related to Lobby')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LobbyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_hint', models.CharField(blank=True, max_length=8000, null=True)),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lobby', to='game.lobby')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='game.question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(choices=[('true', 'true'), ('barely-true', 'barely-true'), ('false', 'false'), ('mostly-true', 'mostly-true'), ('pants-fire', 'pants-fire')], max_length=256)),
                ('is_correct', models.BooleanField(default=False)),
                ('questionid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.question', verbose_name='related to Question')),
            ],
        ),
    ]
