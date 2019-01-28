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
    players = models.ManyToManyField(
        User,
        related_name='quizes',
    )

    @property
    def active_round(self):
        # if round:
        #     self.rounds.update(is_active=False)
        #     round.is_active = True
        #     round.save()
        #     return round

        for round in self.rounds.all():
            if round.is_active:
                return round
        return None

    def __str__(self):
        """ string representation """
        if self.title:
            return "Quiz: {}".format(self.title)
        else:
            return "Quiz: unnamed quiz"


class Round(models.Model):
    class Meta:
        ordering = ['multiplier']
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
    active_question = models.IntegerField(
        null=True,
        default=None,
    )

    def __str__(self):
        """ string representation """
        if self.title:
            return "Round: {}".format(self.title)

    # def active_question(self):
    #     return self.questions.filter(
    #         status__in=[Question.BLUFF, Question.GUESS]).first()

    def reset(self):
        for question in self.questions.all():
            question.reset()
        self.active_question = None
        self.save()

    def first_question(self):
        first = self.questions.filter(
            status=0,
        ).first()
        if first:
            first.status = Question.BLUFF
            first.save()
            return True
        return False

    def next_question(self):
        if self.active_question:
            active = self.questions.get(id=self.active_question)
            if active is not self.questions.last():
                next = self.questions.filter(
                    order__gte=active.order,
                ).exclude(
                    id=active.id,
                ).first()
        else:
            next = self.questions.first()

        if next:
            self.active_question = next.id
            self.save()
            if next.status == Question.INACTIVE:
                next.status = Question.BLUFF
                next.save()

    def prev_question(self):
        if self.active_question:
            active = self.questions.get(id=self.active_question)
            if active is not self.questions.last():
                prev = self.questions.filter(
                    order__lt=active.order,
                ).exclude(
                    id=active.id,
                ).last()
        else:
            prev = self.questions.first()

        if prev:
            self.active_question = prev.id
            self.save()
            if prev.status == Question.INACTIVE:
                prev.status = Question.BLUFF
                prev.save()


class Question(models.Model):
    class Meta:
        ordering = ['order', 'id']

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
    url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        """ string representation """
        return "Question: {}".format(self.text)

    def list_answers(self):
        """Create's a new list of possible answers"""
        # Check if all players have bluffed
        if not len(self.bluffs.all()) == len(self.round.quiz.players.all()):
            return False
        # Check if not already listed
        if self.status >= Question.GUESS:
            return False

        for answer in self.answers.all():
            answer.delete()
        Answer.objects.create(
            question=self,
            text=self.correct_answer,
            is_correct=True,
        )
        for bluff in self.bluffs.all():
            answer = Answer.objects.filter(
                question=self,
                text__iexact=bluff.text).first()
            if answer is None:
                answer = Answer.objects.create(
                    question=self,
                    text=bluff.text)

            bluff.answer = answer
            bluff.save()
        answers = [answer for answer in self.answers.all()]
        random.shuffle(answers)
        i = 0
        for answer in answers:
            answer.order = i = i + 1
            answer.save()

        self.status = Question.GUESS
        self.save()
        return True

    def hide_answers(self):
        if self.status < Question.FINISHED:
            # self.guesses.delete()
            self.answers.all().delete()

            self.status = Question.BLUFF
            self.save()
            return True

    def players_without_guess(self):
        return [
            player for player in self.round.quiz.players.all()
            if len(player.guesses.filter(answer__question=self)) == 0]

    def players_without_bluff(self):
        return [
            player for player in self.round.quiz.players.all()
            if len(player.bluffs.filter(question=self)) == 0]

    def finish(self):
        """Finish the question if all playes have guessed"""
        # TODO: Check if all players have guessed
        if len(self.players_without_guess()) == 0:
            self.status = Question.FINISHED
            self.save()
            return True
        return False

    def reset(self):
        self.status = Question.INACTIVE
        self.bluffs.all().delete()
        self.save()


class Answer(models.Model):
    class Meta:
        ordering = ['order']

    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    order = models.IntegerField(null=True)
    text = models.CharField(
        max_length=255,
    )
    showed = models.BooleanField(
        default=False,
    )
    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        """ string representation """
        return "{}: Answer {}".format(self.question.text, self.order)


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
        blank=True,
        on_delete=models.SET_NULL,
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
    for round in quiz.rounds.all():
        score += score_for_round(player, round)
    return score


def score_for_round(player, round):
    score = 0
    for question in round.questions.all():
        score += score_for_question(player, question)
    return score


def score_for_question(player, question):
    score = 0
    # only finnished questions have scores
    if question.status != Question.FINISHED:
        return 0

    player_bluff = question.bluffs.filter(
        player=player,
        question=question).first()
    player_guess = Guess.objects.filter(
        answer__question=question,
        player=player).first()

    # 0 plunten als jouw bluff = correct antwoord
    if player_bluff.answer.is_correct is True:
        return 0
    # 0 punten als je op je eigen antwoord stemtgit
    if player_guess.answer == player_bluff.answer:
        return 0

    # score voor juist antwoord
    if player_guess.answer.text == question.correct_answer:
        score += question.round.multiplier * 1000

    score += score_for_bluff(player, player_bluff)

    return score


def score_for_bluff(player, bluff):
    score = 0

    player_guess = Guess.objects.filter(
        answer__question=bluff.question,
        player=player).first()

    # 0 plunten als jouw bluff = correct antwoord
    if bluff.answer.is_correct is True:
        return 0
    # 0 punten als je op je eigen antwoord stemtgit
    if player_guess.answer == bluff.answer:
        return 0

    # score voor anders spelers kiezen jouw bluff
    aantal_gepakt = len(Guess.objects.filter(answer=bluff.answer))

    score += (aantal_gepakt * bluff.question.round.multiplier * 500) / len(
        Bluff.objects.filter(answer=bluff.answer))

    return score
