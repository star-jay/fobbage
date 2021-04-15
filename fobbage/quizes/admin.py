# from django.utils.html import format_html
# from django.urls import reverse, path
from django.contrib.admin import register, TabularInline, ModelAdmin, site


from .models import Quiz, Question, Bluff, Guess, Session, Question


class QuestionInline(TabularInline):
    model = Question


class BluffInline(TabularInline):
    model = Bluff


@register(Quiz)
class QuizAdmin(ModelAdmin):
    inlines = (QuestionInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form


site.register(Bluff)
site.register(Guess)
site.register(Session)
site.register(Question)
