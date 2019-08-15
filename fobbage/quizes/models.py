"""
The different models that together make out a quiz
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .messages import round_reset, quiz_updated

User = get_user_model()


class Quiz(models.Model):
    title = models.CharField(
        max_length=255,
    )
    players = models.ManyToManyField(
        User,
        related_name='quizes_playing',
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    active_question = models.ForeignKey(
        to='quizes.Question',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL
    )

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

    def __str__(self):
        """ string representation """
        if self.title:
            return "Round: {}".format(self.title)

    def reset(self):
        for question in self.questions.all():
            question.reset()
        self.save()
        # message
        round_reset(self.quiz.id)

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
        # current active question in this round?
        if self.quiz.active_question.round == self:
            active = self.quiz.active_question
            if active is not self.questions.last():
                next = self.questions.filter(
                    order__gte=active.order,
                ).exclude(
                    id=active.id,
                ).first()
        else:
            next = self.questions.first()

        if next:
            self.quiz.active_question = next
            self.quiz.save()
            self.save()

    def prev_question(self):
        if self.quiz.active_question.round == self:
            active = self.quiz.active_question
            if active is not self.questions.last():
                prev = self.questions.filter(
                    order__lt=active.order,
                ).exclude(
                    id=active.id,
                ).last()
        else:
            prev = self.questions.first()

        if prev:
            self.quiz.active_question = prev
            self.quiz.save()
            self.save()


class Question(models.Model):
    class Meta:
        ordering = ['order', 'id']

    # INACTIVE = 0
    BLUFF, GUESS, FINISHED = range(3)
    STATUS_CHOICES = (
        # (INACTIVE, 'Inactive'),
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
        self.status = Question.BLUFF
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


@receiver(post_save, sender=Quiz)
def quiz_update_signal(sender, instance, created, **kwargs):
    if created:
        quiz_updated(instance.id)
    else:
        quiz_updated(instance.id)


@receiver(post_save, sender=Question)
def question_updated_signal(sender, instance, created, **kwargs):
    if created:
        quiz_updated(instance.round.quiz.id)
    else:
        quiz_updated(instance.round.quiz.id)
