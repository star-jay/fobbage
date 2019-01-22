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
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        """ string representation """
        if self.title:
            return "Round: {}".format(self.title)

    def active_question(self):
        return self.questions.get(
            status__in=[Question.BLUFF, Question.GUESS])

    def first_question(self):
        first = self.questions.get(order=1)
        first.status = Question.BLUFF
        first.save()

    def next_question(self):
        active = self.active_question()
        if active:
            next = self.questions.get(
                order=active.order+1)
            active.status = Question.FINISHED
            active.save()
        else:
            next = self.questions.order('order').first()

        if next:
            next.status = Question.BLUFF
            next.save()


class Question(models.Model):
    INACTIVE = 0
    BLUFF = 1
    GUESS = 2
    FINISHED = 3
    STATUS_CHOICES = (
        (INACTIVE, 'Inactive'),
        (BLUFF, 'Bluff'),
        (GUESS, 'Guess'),
        (FINISHED, 'Finished'),
    )
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
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0
    )
    order = models.IntegerField()

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


class Guess(models.Model):
    answer = models.ForeignKey(
        Answer,
        related_name='guesses',
        on_delete=models.CASCADE,
    )

    player = models.ForeignKey(
        User,
        related_name='guesses',
        on_delete=models.CASCADE,
    )


def score_for_quiz(player, quiz):

    score = 0
    for round in quiz.rounds:
        score += score_for_round(player, round)

    return score


def score_for_round(player, round):
    score = 0
    for question in round.questions:
        score += score_for_question(player, question)


def score_for_question(player, question):
    score = 0
    player_bluff = question.bluffs.filter(player=player)
    # 0 plunten als jouw bluff = correct antwoord
    if question.correct_answer == player_bluff:
        return 0
    # score voor juist antwoord
    my_guess = Guess.objects.filter(
        player=player)

    if my_guess.answer.text == question.correct_answer:
        score += question.round.multiplier * 1000

    # score voor anders spelers kiezen jouw bluff
    aantal_gepakt = len(Guess.objects.filter(answer=player_bluff.answer))

    score += (aantal_gepakt * question.round.multiplier * 500) / len(
        Bluff.objects.filter(answer=player_bluff.answer))

    return score


# def score_for_answer(play, answer):

