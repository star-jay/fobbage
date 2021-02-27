from django.urls import path, include
from rest_framework.routers import DefaultRouter

from fobbage.quizes.views import (
    SessionViewSet, FobbitViewSet,
    AnswerViewSet, QuizViewSet, ActiveFobbitViewSet, BluffViewSet,
    GuessViewSet,
)


router = DefaultRouter()
router.register(r'quizes', QuizViewSet, basename='quiz')
router.register(r'fobbits', FobbitViewSet, basename='fobbit')
router.register(r'sessions', SessionViewSet, basename='session')

router.register(r'bluffs', BluffViewSet, basename='bluff')
router.register(r'guesses', GuessViewSet, basename='guess')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(
    r'active_fobbits', ActiveFobbitViewSet, basename='active_fobbit')

urlpatterns = [
    path('', include(router.urls)),
]
