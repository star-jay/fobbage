from django.urls import path, include
from rest_framework.routers import DefaultRouter

from fobbage.quizes.views import (
    SessionViewSet, FobbitViewSet,
    # API
    AnswerViewSet, QuizViewSet, ActiveQuestionViewSet, BluffViewSet,
    GuessViewSet,
)


router = DefaultRouter()
router.register(r'quizes', QuizViewSet, basename='quiz')
router.register(r'fobbit', FobbitViewSet, basename='fobbit')
router.register(r'session', SessionViewSet, basename='session')

router.register(r'bluffs', BluffViewSet, basename='bluff')
router.register(r'guesses', GuessViewSet, basename='guess')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(
    r'active_questions', ActiveQuestionViewSet, basename='active_question')

urlpatterns = [
    path('', include(router.urls)),
]
