from django.shortcuts import render
from django.views.generic import ListView

from fobbage.quizes.models import Quiz, Round


class RoundListView(ListView):
    template_name = 'quizes/rounds.html'
    model = Round


def index(request):
    active_quiz_list = Quiz.objects.all()
    context = {
        'active_quiz_list': active_quiz_list
        }
    return render(request, 'quizes/index.html', context)
