"""
The different models that together make out a quiz
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property

from .messages import quiz_updated


User = get_user_model()


class Quiz(models.Model):
    title = models.CharField(
        max_length=255,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """ string representation """
        if self.title:
            return "Quiz: {}".format(self.title)
        else:
            return "Quiz: unnamed quiz"


class Question(models.Model):
    class Meta:
        ordering = ['order', 'id']

    text = models.CharField(
        max_length=255,
    )
    correct_answer = models.CharField(
        max_length=255,
    )
    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE,
    )

    order = models.IntegerField()
    url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    player = models.ForeignKey(
        User,
        related_name='questions',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """ string representation """
        return "Question: {}".format(self.text)


class Session(models.Model):
    # class Meta:

    quiz = models.ForeignKey(
        Quiz,
        related_name='sessions',
        on_delete=models.CASCADE,
    )
    created = models.DateField(auto_now=True)
    name = models.CharField(
        max_length=255,
    )
    owner = models.ForeignKey(
        User,
        related_name='hosting',
        on_delete=models.DO_NOTHING,
    )
    players = models.ManyToManyField(
        User,
        related_name='playing',
    )
    active_fobbit = models.ForeignKey(
        to='quizes.Fobbit',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='active_in'
    )
    BLUFFING, GUESSING = range(2)
    MODI = [
        (BLUFFING, 'Bluffing'),
        (GUESSING, 'Guessing'),
    ]

    modus = models.IntegerField(
        choices=MODI,
        default=BLUFFING,
    )

    def __str__(self):
        return self.name


class Fobbit(models.Model):
    """Combination of session and question"""
    session = models.ForeignKey(
        Session,
        related_name='fobbits',
        on_delete=models.CASCADE,
    )

    question = models.ForeignKey(
        Question,
        related_name='fobbits',
        on_delete=models.CASCADE,
    )
    BLUFF, GUESS, FINISHED = range(3)
    STATUS_CHOICES = (
        (BLUFF, 'Bluff'),
        (GUESS, 'Guess'),
        (FINISHED, 'Finished'),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0
    )

    def __str__(self):
        return self.question.text

    @cached_property
    def multiplier(self):
        if self.question.order > 8:
            return 3
        if self.question.order > 3:
            return 2
        return 1

    @cached_property
    def players_without_guess(self):
        return [
            player for player in self.session.players.all()
            if len(player.guesses.filter(answer__fobbit=self)) == 0]

    @cached_property
    def players_without_bluff(self):
        return [
            player for player in self.session.players.all()
            if len(player.bluffs.filter(fobbit=self)) == 0]

    @property
    def scored_answers(self):
        if self.status == self.FINISHED:
            return self.answers.annotate(
                num_guesses=models.Count('guesses')
            ).order_by('is_correct', 'num_guesses')
        else:
            return self.answers.empty()


class Answer(models.Model):
    class Meta:
        ordering = ['order']

    fobbit = models.ForeignKey(
        Fobbit,
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
        return "{}: Answer {}".format(self.fobbit.question.text, self.order)


class Bluff(models.Model):
    text = models.CharField(
        max_length=255,
    )
    fobbit = models.ForeignKey(
        Fobbit,
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

    class Meta:
        unique_together = ("fobbit", "player"),

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
        quiz_updated(instance.quiz.id)
    else:
        quiz_updated(instance.quiz.id)
