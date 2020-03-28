# from django.utils.html import format_html
# from django.urls import reverse, path
from django.contrib.admin import register, TabularInline, ModelAdmin, site
from django.shortcuts import redirect


from .models import Quiz, Round, Question, Bluff, Guess
from .services import generate_answers


def reset(modeladmin, request, queryset):
    for round in queryset:
        round.reset()


reset.short_description = "reset round"


def generate_answers_action(request, question_id, *args, **kwargs):
    generate_answers(question_id)
    return redirect('/admin/quizes/question/')


class QuestionInline(TabularInline):
    model = Question


class RoundInline(TabularInline):
    model = Round


class BluffInline(TabularInline):
    model = Bluff


# @register(Question)
# class QuestionAdmin(ModelAdmin):
#     model = Question
#     # inlines = (BluffInline,)

#     list_display = (
#         'round',
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


@register(Round)
class RoundAdmin(ModelAdmin):
    model = Round
    inlines = (QuestionInline,)
    actions = [reset, ]


@register(Quiz)
class QuizAdmin(ModelAdmin):
    inlines = (RoundInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            questions = Question.objects.filter(round__quiz=obj)
        else:
            questions = Question.objects.none()

        form.base_fields['active_question'].queryset = questions
        form.base_fields['active_question'].required = False

        return form


site.register(Bluff)
site.register(Guess)
