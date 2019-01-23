from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import viewsets
from fobbage.quizes.models import Quiz, Round, Question, Answer
from fobbage.quizes.api.serializers import QuizSerializer


def index(request):
    active_quiz_list = Quiz.objects.all()
    context = {
        'active_quiz_list': active_quiz_list
        }
    return render(request, 'quizes/index.html', context)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetail(DetailView):
    template_name = 'quizes/quiz.html'
    model = Quiz


# class RoundDetail(DetailView):
#     template_name = 'quizes/round.html'
#     model = Round
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
