"""
The different models that together make out a quiz
"""
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.db.models import OuterRef
from django.dispatch import receiver

from .messages import session_updated

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
    image_url = models.CharField(
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
    settings = models.JSONField(default=dict)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def rounds(self):
        try:
            rounds = self.settings.get('rounds', [])
            if type(rounds) == list:
                return rounds
            else:
                return []
            # return rounds[self.settings.get('activeRound', 10)]
        except KeyError:
            return []

    @property
    def active_round(self):
        try:
            if self.active_fobbit:
                return self.active_fobbit.round
        except KeyError:
            return -1

        return -1

    def questions_in_round(self, round):
        # active round
        try:
            return self.rounds[round]['number_of_questions']
        except (IndexError, KeyError, TypeError):
            return 0

    # move to manager
    def next_question(self):
        # While bluffing, create a new fobbit out of available questions
        fobbit = None

        max_questions = self.questions_in_round(round=self.active_round)
        n_of_questions = self.fobbits.filter(round=self.active_round).count()

        if self.modus == self.BLUFFING:
            if n_of_questions < max_questions:
                fobbit = self.generate_fobbit(round=self.active_round)
            else:
                # Go back to guessing
                self.modus = self.GUESSING
                fobbit = self.fobbits.filter(round=self.active_round).first()

        if fobbit:
            self.active_fobbit = fobbit

        self.save()
        return fobbit

    # move to manager
    def generate_fobbit(self, round):
        questions = self.quiz.questions.exclude(
                id__in=[self.fobbits.values_list('question', flat=True)]
            )
        question = questions.first()

        return Fobbit.objects.create(
            question=question,
            session=self,
            round=round,
        )

    def new_round(self, round):
        rounds = self.rounds
        rounds.append(round)

        self.settings['rounds'] = rounds
        self.active_fobbit = self.generate_fobbit(round=len(rounds)-1)
        # return to guessing
        self.modus = 0
        self.save()

    def score_for_player(self, player):
        score = Score.objects.filter(
            fobbit__session=self,
            user=player,).aggregate(score=models.Sum('score')).get('score', 0)
        return score or 0

    def likes_for_player(self, player):
        return LikeAnswer.objects.filter(
            answer__fobbit__session=self,
            answer__bluffs__player=player,
        ).exclude(player=player).count()


class Fobbit(models.Model):
    """Combination of session and question"""

    class Meta:
        ordering = ['id']

    BLUFF, GUESS, FINISHED = range(3)
    STATUS_CHOICES = (
        (BLUFF, 'Bluff'),
        (GUESS, 'Guess'),
        (FINISHED, 'Finished'),
    )

    question = models.ForeignKey(
        Question,
        related_name='fobbits',
        on_delete=models.CASCADE,
    )

    session = models.ForeignKey(
        Session,
        related_name='fobbits',
        on_delete=models.CASCADE,
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0
    )

    players = models.ManyToManyField(
        User,
        related_name='fobbits',
        through='Score',
    )

    # integer, round details are stored in the session
    round = models.IntegerField(default=0)

    def __str__(self):
        return self.question.text

    @property
    def multiplier(self):
        # get the multiplier from the round
        if self.session.rounds:
            try:
                return self.session.rounds[self.round]['multiplier']
            except IndexError:
                return self.round + 1
        else:
            return 1

    @property
    def players_without_guess(self):
        return self.session.players.exclude(
            id__in=Guess.objects.filter(
                player=OuterRef('pk'),  # Assuming player is a ForeignKey in the Guess model
                answer__fobbit=self
            ).values('player')
        )

    @property
    def players_without_bluff(self):
        return self.session.players.exclude(
            id__in=Bluff.objects.filter(
                player=OuterRef('pk'),  # Assuming player is a ForeignKey in the Guess model
                fobbit=self
            ).values('player')
        )

    def generate_answers(self):
        """
        Creates a new list of possible answers
        use a combination of bluffs and the correct answer
        """
        if len(self.session.players.all()) == 0:
            return False

        # Check if all players have bluffed
        if self.session.players.exclude(bluffs__fobbit=self).count() >0:
            return False
        # Check if not already listed
        if self.status >= self.GUESS:
            return False

        for answer in self.answers.all():
            answer.delete()

        Answer.objects.create(
            fobbit=self,
            text=self.question.correct_answer,
            is_correct=True,
        )

        for bluff in self.bluffs.all():
            answer = self.answers.filter(text__iexact=bluff.text).first()
            if answer is None:
                answer = Answer.objects.create(
                    fobbit=self,
                    text=bluff.text)

            bluff.answer = answer
            bluff.save()

        answers = [answer for answer in self.answers.all()]
        random.shuffle(answers)
        i = 0
        for answer in answers:
            answer.order = i = i + 1
            answer.save()

        self.status = Fobbit.GUESS
        self.save()

        return True

    def score_for_player(self, player):
        score = 0
        # only finnished questions have scores
        if self.status != self.FINISHED:
            return 0

        try:
            player_bluff = self.bluffs.get(player=player)
        except Bluff.DoesNotExist:
            player_bluff = None

        # als de speler heeft gebluffed
        if player_bluff:
            # 0 plunten als jouw bluff = correct antwoord
            if player_bluff.answer and player_bluff.answer.is_correct is True:
                return 0

            score += player_bluff.score

        try:
            player_guess = Guess.objects.get(
                answer__fobbit=self, player=player)
        except Guess.DoesNotExist:
            player_guess = None

        # score voor juist antwoord
        if player_guess is not None:
            if player_bluff and player_guess.answer == player_bluff.answer:
                return 0
            if player_guess.answer.text == self.question.correct_answer:
                score += player_guess.score

        return score

    def reset(self):
        self.status = Fobbit.BLUFF
        self.answers.all().delete()
        self.save()

    # FOBBIT
    def finish(self):
        """Finish the question if all players have guessed"""

        if len(self.players_without_guess) == 0:
            self.status = self.FINISHED
            self.save()

            self.update_scores()

        else:
            raise Guess.DoesNotExist("Not all players have guessed")

    def update_scores(self):
        # update scores
        self.scores.all().delete()

        for player in self.session.players.all():
            Score.objects.create(
                user=player,
                fobbit=self,
                score=self.score_for_player(player)
            )

    def delete_answers(self):
        if self.status < self.FINISHED:
            # self.guesses.delete()
            self.answers.all().delete()

            self.status = self.BLUFF
            self.save()
            return True


class Score(models.Model):
    """
    Keeps track of the score for a player in a fobbit
    """
    user = models.ForeignKey(
        User,
        related_name='scores',
        on_delete=models.CASCADE,)
    fobbit = models.ForeignKey(
        Fobbit,
        related_name='scores',
        on_delete=models.CASCADE,)
    score = models.IntegerField(default=0)


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

    @property
    def score(self):
        # zero points if your this was the correct answer
        if self.answer and self.answer.is_correct:
            return 0

        # zero points if you vote for your own bluff
        if self.answer.guesses.filter(player=self.player).exists():
            return 0

        # Get points when people vote on this bluff
        tricked_count = self.answer.guesses.count()

        score = tricked_count * self.fobbit.multiplier * 500
        # devide by people with the same bluff
        score = score / self.answer.bluffs.count()

        return score

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

    @property
    def score(self):
        fobbit = self.answer.fobbit
        if fobbit.status == fobbit.FINISHED:
            if self.answer.text == fobbit.question.correct_answer:
                return fobbit.multiplier * 1000
        else:
            return 0


@receiver(post_save, sender=Session)
def session_updated_signal(sender, instance, created, **kwargs):
    if kwargs['raw']:
        return
    session_updated(instance.id)


@receiver(post_save, sender=Fobbit)
def fobbit_updated_signal(sender, instance, created, **kwargs):
    if kwargs['raw']:
        return
    session_updated(instance.session.id)


@receiver(post_save, sender=Bluff)
def bluff_updated_signal(sender, instance, created, **kwargs):
    if kwargs['raw']:
        return
    session_updated(instance.fobbit.session.id)
    # everyone bluffed?
    if created:
        # niet bij eerste vraag
        if len(instance.fobbit.session.fobbits.all()) > 1:
            if len(instance.fobbit.bluffs.all()) == len(
                    instance.fobbit.session.players.all()):
                if instance.fobbit.generate_answers():
                    instance.fobbit.session.next_question()


@receiver(post_save, sender=Guess)
def guess_updated_signal(sender, instance, created, **kwargs):
    if kwargs['raw']:
        return
    session_updated(instance.answer.fobbit.session.id)


@receiver(post_save, sender=Answer)
def _updated_signal(sender, instance, created, **kwargs):
    if kwargs['raw']:
        return
    session_updated(instance.fobbit.session.id)

class LikeAnswer(models.Model):
    answer = models.ForeignKey(
        Answer,
        related_name='likeAnswers',
        on_delete=models.CASCADE,
    )

    player = models.ForeignKey(
        User,
        related_name='likeAnswers',
        on_delete=models.CASCADE,
    )

    @property
    def score(self):
        fobbit = self.answer.fobbit
        if fobbit.status == fobbit.FINISHED:
            return 1;
        else:
            return 0
