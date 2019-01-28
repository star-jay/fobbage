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
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from fobbage.quizes.views import (
    QuizViewSet, AnswerViewSet, BluffView,
    QuizDetail, round_view, index, show_answers, scoreboard, hide_answers,
    next_question, prev_question, first_question, show_scores, GuessView
)

router = DefaultRouter()
router.register(r'quizes', QuizViewSet)
# router.register(r'bluffs', BluffViewSet, base_name='bluff')
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', index, name='index'),
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
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    # url(r'^accounts/', include('allauth.urls')),

    path('api/', include(router.urls)),
    path('api/', include('fobbage.accounts.api.urls')),
    path('api-auth/', include('rest_framework.urls')),

    path('api/bluffs/', BluffView.as_view(), name='bluff'),
    path('api/guess/', GuessView.as_view(), name='bluff'),

]
