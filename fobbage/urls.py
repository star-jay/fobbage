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

from fobbage.quizes.views import (
    quiz_view, index, session_play, scoreboard, new_quiz, collect_answers,
    hide_answers, next_question, prev_question, show_scores, session_join,
    QuizList, start_guessing, start_bluffing, session_view,
    SessionCreateView, SessionJoin, SessionContinue,
    SessionUpdate, reset_fobbit,
)
# from fobbage.accounts.views import CreateUserView
from fobbage.accounts.views import signup


urlpatterns = [
    path('', index, name='index'),
    path('api/', include('fobbage.accounts.urls')),
    path('api/', include('fobbage.quizes.urls')),

    path('new_quiz/', new_quiz, name='new_quiz'),
    path('new_session/', SessionCreateView.as_view(), name='new_quiz'),

    path('host/', QuizList.as_view()),
    path('join/', SessionJoin.as_view()),
    path('continue/', SessionContinue.as_view()),

    path('quiz/<int:quiz_id>/', quiz_view, name='quiz'),

    path('session/<int:session_id>/', session_view, name='session'),
    path('session/<int:session_id>/join/', session_join, name='join'),
    path('session/<int:session_id>/play/', session_play, name='play'),
    path('session/<int:session_id>/scoreboard', scoreboard, name='scoreboard'),
    path(
        'session/<int:session_id>/update',
        SessionUpdate.as_view(),
        name='scoreboard'),


    path(
        'session/<int:session_id>/next_question', next_question,
        name='next_question'),
    path(
        'session/<int:session_id>/prev_question', prev_question,
        name='prev_question'),

    path(
        'session/<int:session_id>/start_guessing/',
        start_guessing,
        name='start_guessing'),
    path(
        'session/<int:session_id>/start_bluffing/',
        start_bluffing,
        name='start_bluffing'),
    # path(
    #     'question/<int:question>/collect_answers/',
    #     show_answers,
    #     name='show_answers'),
    path(
        'question/<int:question>/hide_answers/',
        hide_answers,
        name='hide_answers'),
    path(
        'fobbit/<int:fobbit_id>/collect_answers/',
        collect_answers,
        name='collect_answers'),
    path(
        'fobbit/<int:fobbit_id>/reset/',
        reset_fobbit,
        name='reset'),
    path(
        'fobbit/<int:fobbit_id>/show_scores/',
        show_scores,
        name='show_scores'),
    path('api/accounts/', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    # path('login/', auth_views.login, name='login'),
    # path('api/register', CreateUserView.as_view(), name="create-user"),
    # path('api/', include('fobbage.accounts.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
