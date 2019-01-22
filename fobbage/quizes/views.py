from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import viewsets
from fobbage.quizes.models import Quiz, Round, Question
from fobbage.quizes.api.serializers import QuizSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetail(DetailView):
    template_name = 'quizes/quiz_detail.html'
    model = Quiz


class RoundDetail(DetailView):
    template_name = 'quizes/round_detail.html'
    model = Round


def next_question(self, pk):
    round = Round.objects.get(id=pk)
    round.next_question()
    return HttpResponseRedirect(reverse('round', args=(round.id,)))


def first_question(self, pk):
    round = Round.objects.get(id=pk)
    round.first_question()
    return HttpResponseRedirect(reverse('round', args=(round.id,)))


class QuestionDetail(DetailView):
    template_name = 'quizes/question_detail.html'
    model = Question


def index(request):
    active_quiz_list = Quiz.objects.all()
    context = {
        'active_quiz_list': active_quiz_list
        }
    return render(request, 'quizes/index.html', context)


def show_answers(request, question):
    question = Question.objects.get(pk=question)
    question.list_answers()
    context = {'question': question}
    return render(
        request, 'quizes/question_detail.html', context)
