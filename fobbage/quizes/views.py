from django.shortcuts import render
from fobbage.quizes.models import Quiz


def index(request):
    active_quiz_list = Quiz.objects.all()
    context = {
        'active_quiz_list': active_quiz_list 
        } 
    return render(request, 'quizes/index.html', context)