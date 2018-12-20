"""
The different models that together make out a quiz
"""
import random
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
    multiplier = models.FloatField(
        default=1,
    )

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

    def list_answers(self):
        """Create's a new list of possible answers"""
        for answer in self.answers.all():
            answer.delete()
        Answer.objects.create(
            question=self,
            text=self.correct_answer
        )
        for bluff in self.bluffs.all():
            answer = Answer.objects.create(
                question=self,
                text=bluff.text
            )
            bluff.answer = answer
        answers = [answer for answer in self.answers.all()]
        random.shuffle(answers)
        for index in range(len(answers)):
            answers[index].round = index + 1


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    order = models.IntegerField(null=True)
    text = models.CharField(
        max_length=255,
    )

    def __str__(self):
        """ string representation """
        return "{}: {}".format(self.order, self.text)


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
    answer = models.ForeignKey(
        Answer,
        related_name='bluffs',
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """ string representation """
        return "{}: {}".format(self.player.first_name, self.text)
