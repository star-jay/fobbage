# from django.utils.html import format_html
# from django.urls import reverse, path
from django.contrib.admin import register, TabularInline, ModelAdmin, site
from django.shortcuts import redirect


from .models import Quiz, Question, Bluff, Guess, Session
from .services import generate_answers


def generate_answers_action(request, question_id, *args, **kwargs):
    generate_answers(question_id)
    return redirect('/admin/quizes/question/')


class QuestionInline(TabularInline):
    model = Question


class BluffInline(TabularInline):
    model = Bluff


# @register(Question)
# class QuestionAdmin(ModelAdmin):
#     model = Question
#     # inlines = (BluffInline,)

#     list_display = (
#         'text',
#         'status',
#         'question_actions',
#     )

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path(
#                 '<int:question_id>/generate_answers/',
#                 generate_answers_action,
#                 name='generate_answers',
#             ),
#         ]
#         return custom_urls + urls

#     def question_actions(self, obj):
#         return format_html(
#             '<a class="button" href="{}">Generate Answers</a>&nbsp',
#             reverse('admin:generate_answers', args=[obj.pk]),
#         )


@register(Quiz)
class QuizAdmin(ModelAdmin):
    inlines = (QuestionInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form


site.register(Bluff)
site.register(Guess)
site.register(Session)
