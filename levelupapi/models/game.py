from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=55)
    maker = models.CharField(max_length=55)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
