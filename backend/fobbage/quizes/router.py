from django.urls import path, include
from rest_framework.routers import DefaultRouter

from fobbage.quizes.views import (
    SessionViewSet, FobbitViewSet,
    AnswerViewSet, QuizViewSet, ActiveFobbitViewSet, BluffViewSet,
    GuessViewSet, LikeAnswerViewSet, QuestionViewSet,
)

__all__ = ['router']


router = DefaultRouter()
router.register(r'quizes', QuizViewSet, basename='quiz')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'fobbits', FobbitViewSet, basename='fobbit')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'bluffs', BluffViewSet, basename='bluff')
router.register(r'guesses', GuessViewSet, basename='guess')
router.register(r'like-answers', LikeAnswerViewSet, basename='like_answer')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(
    r'active_fobbits', ActiveFobbitViewSet, basename='active_fobbit')

