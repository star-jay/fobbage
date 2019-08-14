"""fobbage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.contrib import auth as auth_views
from django.urls import path, include
# from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from fobbage.quizes.views import (
    round_view, index, play, show_answers, scoreboard, new_quiz,
    hide_answers, next_question, prev_question, first_question, show_scores,
    QuizDetail, QuizList,
    # API
    AnswerViewSet, QuizViewSet, ActiveQuestionViewSet, BluffViewSet, GuessViewSet,
)
# from fobbage.accounts.api.views import CreateUserView
from fobbage.accounts.views import signup


router = DefaultRouter()
router.register(r'quizes', QuizViewSet, base_name='quiz')
router.register(r'bluffs', BluffViewSet, base_name='bluff')
router.register(r'guesses', GuessViewSet, base_name='guess')
router.register(r'answers', AnswerViewSet, base_name='answer')
router.register(
    r'active_questions', ActiveQuestionViewSet, base_name='active_question')


urlpatterns = [

    path('', index, name='index'),
    path('new_quiz/', new_quiz, name='new_quiz'),
    path('host/', QuizList.as_view()),
    path('play/', play, name='play'),

    path('quiz/<int:pk>/', QuizDetail.as_view()),
    path('quiz/<int:pk>/scoreboard', scoreboard, name='scoreboard'),
    path('round/<int:round>/', round_view, name='round'),
    path('round/<int:pk>/next_question', next_question, name='next_question'),
    path('round/<int:pk>/prev_question', prev_question, name='prev_question'),

    path(
        'round/<int:pk>/first_question',
        first_question,
        name='first_question'),
    # path('question/<int:pk>/', QuestionDetail.as_view()),

    path(
        'question/<int:question>/show_answers/',
        show_answers,
        name='show_answers'),
    path(
        'question/<int:question>/hide_answers/',
        hide_answers,
        name='hide_answers'),
    path(
        'question/<int:question>/show_scores/',
        show_scores,
        name='show_scores'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
    # path('accounts/register', CreateUserView.as_view(), name="create-user"),
    path('signup/', signup, name='signup'),
    # path('login/', auth_views.login, name='login'),
    path('api/', include(router.urls)),
    path('api/', include('fobbage.accounts.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
