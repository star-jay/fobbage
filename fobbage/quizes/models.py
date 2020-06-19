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

    def next_question(self):
        if self.active_fobbit:
            active = self.active_fobbit.question
            next = self.quiz.questions.filter(
                    order__gte=active.order,
                ).exclude(id=active.id).first()
        else:
            next = self.quiz.questions.first()

        fobbit = Fobbit.objects.create(
            question=next,
            session=self,
        )
        self.active_fobbit = fobbit
        self.save()
        return fobbit

    def prev_question(self):
        active = self.active_fobbit
        if active:
            if active is not self.questions.first():
                self.active_fobbit = self.fobbits.filter(
                        question__order__lte=active.question.order,
                    ).exclude(
                        id=active.id,
                    ).last()
                self.save()


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

    @cached_property
    def multiplier(self):
        return 1

    def hide_answers(self):
        if self.status < Fobbit.FINISHED:
            # self.guesses.delete()
            self.answers.all().delete()

            self.status = Fobbit.BLUFF
            self.save()
            return True

    def players_without_guess(self):
        return [
            player for player in self.session.players.all()
            if len(player.guesses.filter(answer__fobbit=self)) == 0]

    def players_without_bluff(self):
        return [
            player for player in self.session.players.all()
            if len(player.bluffs.filter(fobbit=self)) == 0]

    def finish(self):
        """Finish the question if all players have guessed"""
        # TODO: Check if all players have guessed
        if len(self.players_without_guess()) == 0:
            self.status = Fobbit.FINISHED
            self.save()
            return True
        return False

    def reset(self, session):
        self.status = Fobbit.BLUFF
        self.bluffs.all().delete()
        self.save()


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
