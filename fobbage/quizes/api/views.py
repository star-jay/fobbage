from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import DetailView
from django.db.models import Count
from rest_framework import viewsets, generics
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


class QuizDetail(DetailView):
    template_name = 'quizes/quiz.html'
    model = Quiz
