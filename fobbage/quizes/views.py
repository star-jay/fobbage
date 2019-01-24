from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import viewsets, generics
from rest_framework.mixins import (
    CreateModelMixin, RetrieveModelMixin, UpdateModelMixin)
from fobbage.quizes.models import Quiz, Round, Question, Answer, Bluff, score_for_quiz
from fobbage.quizes.api.serializers import (
    QuizSerializer, BluffSerializer, AnswerSerializer)


# API
class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class BluffViewSet(
        viewsets.GenericViewSet, CreateModelMixin, RetrieveModelMixin,
        UpdateModelMixin):
    # queryset = Bluff.objects.all()
    serializer_class = BluffSerializer

    def get_queryset(self):
        return Bluff.objects.all()


# Quizmaster
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


def show_scores(request, question):
    question = Question.objects.get(pk=question)
    if question.finish():
        answer = Answer.objects.filter(
            question=question).first()
        context = {'answer': answer}
        return render(
            request, 'quizes/scores.html', context)
    else:
        return HttpResponseRedirect(
            reverse('round', args=(question.round.id,)))


def scoreboard(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    scores = {
        player: score_for_quiz(player, quiz)
        for player in quiz.players.all()
    }
    ranking = sorted(scores, key=scores.__getitem__)
    ranked_scores = [(player, scores[player]) for player in ranking]
    context = {
        'scores': ranked_scores,
        # 'ranking': ranking,
    }
    return render(
        request, 'quizes/leaderboard.html', context)
