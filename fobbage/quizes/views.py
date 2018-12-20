from django.shortcuts import render
from django.views.generic import DetailView

from fobbage.quizes.models import Quiz, Round, Question


class QuizDetail(DetailView):
    template_name = 'quizes/quiz_detail.html'
    model = Quiz


class RoundDetail(DetailView):
    template_name = 'quizes/round_detail.html'
    model = Round


class QuestionDetail(DetailView):
    template_name = 'quizes/question_detail.html'
    model = Question


def index(request):
    active_quiz_list = Quiz.objects.all()
    context = {
        'active_quiz_list': active_quiz_list
        }
    return render(request, 'quizes/index.html', context)
