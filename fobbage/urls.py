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
from django.urls import path

from fobbage.quizes.views import (
    QuizDetail, RoundDetail, QuestionDetail, index
)


urlpatterns = [
    path('', index, name='index'),
    path('quiz/<int:pk>/', QuizDetail.as_view()),
    path('round/<int:pk>/', RoundDetail.as_view()),
    path('question/<int:pk>/', QuestionDetail.as_view()),
    path('admin/', admin.site.urls),
]
