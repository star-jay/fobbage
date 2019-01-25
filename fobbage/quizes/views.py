from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import DetailView
from django.db.models import Count
from rest_framework import viewsets, generics
from rest_framework.mixins import (
    CreateModelMixin, RetrieveModelMixin, UpdateModelMixin)
from fobbage.quizes.models import (
    Quiz, Round, Question, Answer, Bluff,
    score_for_quiz, score_for_bluff, Guess)
from fobbage.quizes.api.serializers import (
    QuizSerializer, BluffSerializer, AnswerSerializer, GuessSerializer)


# API
class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class BluffView(generics.CreateAPIView):
    serializer_class = BluffSerializer

    def get_queryset(self):
        if self.request.user:
            return Bluff.objects.filter(player=self.request.user)
        else:
            return Bluff.objects.none()

    def post(self, request, *args, **kwargs):
        return self.create(
            request, player=request.user, *args, **kwargs)


class GuessView(generics.CreateAPIView):
    serializer_class = GuessSerializer

    def get_queryset(self):
        if self.request.user:
            return Guess.objects.filter(player=self.request.user)
        else:
            return Guess.objects.none()

    def post(self, request, *args, **kwargs):
        return self.create(
            request, player=request.user, *args, **kwargs)


def index(request):
    active_quiz_list = Quiz.objects.all()
    context = {
        'active_quiz_list': active_quiz_list
        }
    return render(request, 'quizes/index.html', context)


class QuizDetail(DetailView):
    template_name = 'quizes/quiz.html'
    model = Quiz


def round_view(request, round):
    round = Round.objects.get(pk=round)
    active_round = round.quiz.active_round
    if active_round:
        active_round.is_active = False
        active_round.save()
    round.is_active = True
    round.save()
    context = {'round': round}
    if round.active_question is not None:
        question = Question.objects.get(pk=round.active_question)
        context['question'] = question

    return render(
        request, 'quizes/round.html', context)


def next_question(self, pk):
    round = Round.objects.get(id=pk)
    round.next_question()
    return HttpResponseRedirect(reverse('round', args=(round.id,)))


def prev_question(self, pk):
    round = Round.objects.get(id=pk)
    round.prev_question()
    return HttpResponseRedirect(reverse('round', args=(round.id,)))


def first_question(self, pk):
    round = Round.objects.get(id=pk)
    if round.first_question():
        return HttpResponseRedirect(reverse('round', args=(round.id,)))

    return HttpResponseRedirect(reverse('round', args=(round.id,)))


def show_answers(request, question):
    question = Question.objects.get(pk=question)
    question.list_answers()

    return HttpResponseRedirect(
        reverse('round', args=(question.round.id,)))


def hide_answers(request, question):
    question = Question.objects.get(pk=question)
    question.hide_answers()

    return HttpResponseRedirect(
        reverse('round', args=(question.round.id,)))


def show_scores(request, question):
    question = Question.objects.get(pk=question)
    if question.finish():
        # show player answers
        answer = Answer.objects \
            .filter(
                question=question,
                showed=False,
                is_correct=False) \
            .annotate(num_guesses=Count('guesses')) \
            .order_by('num_guesses') \
            .first()
        if answer:
            answer.showed = True
            answer.save()
        else:
            # reset answer to show again
            Answer.objects.filter(
                question=question).update(
                    showed=False)
            # show correct answer
            answer = Answer.objects.get(
                question=question,
                is_correct=True)
        if answer:
            # bluffs en scores
            if len(answer.bluffs.all()) > 0:
                bluffs = [
                    {
                        'player': bluff.player,
                        'score': score_for_bluff(bluff.player, bluff)
                    } for bluff in answer.bluffs.all()
                ]
            else:
                bluffs = None
            # show the answer

            context = {
                'answer': answer,
                'bluffs': bluffs}
            return render(
                request, 'quizes/scores.html', context)

    return HttpResponseRedirect(
        reverse('round', args=(question.round.id,)))


def scoreboard(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    active_round = quiz.active_round
    scores = {
        player: score_for_quiz(player, quiz)
        for player in quiz.players.all()
    }
    ranking = sorted(scores, key=scores.__getitem__)
    ranked_scores = [(player, scores[player]) for player in ranking]
    context = {
        'scores': ranked_scores,
        'active_round': active_round,
        # 'ranking': ranking,
    }
    return render(
        request, 'quizes/leaderboard.html', context)
