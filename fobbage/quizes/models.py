"""
The different models that together make out a quiz
"""

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Quiz(models.Model):
    title = models.CharField(
        max_length=255,
    )

    def __str__(self):
        """ string representation """
        if self.title:
            return "Quiz: {}".format(self.title)
        else:
            return "Quiz: unnamed quiz"


class Round(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        related_name='rounds',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=255,
    )
    multiplier = models.FloatField()

    def __str__(self):
        """ string representation """
        if self.title:
            return "Round: {}".format(self.title)


class Question(models.Model):
    text = models.CharField(
        max_length=255,
    )
    correct_answer = models.CharField(
        max_length=255,
    )
    round = models.ForeignKey(
        Round,
        related_name='questions',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """ string representation """
        return "Question: {}".format(self.text)


class Bluff(models.Model):
    text = models.CharField(
        max_length=255,
    )
    question = models.ForeignKey(
        Question,
        related_name='bluffs',
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(
        User,
        related_name='bluffs',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """ string representation """
        return "{}: {}".format(self.player.first_name, self.text)
