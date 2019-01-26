from django.contrib import admin

from .models import Quiz, Round, Question, Bluff, Guess


def reset(modeladmin, request, queryset):
    for round in queryset:
        round.reset()


reset.short_description = "reset round"


class QuestionInline(admin.TabularInline):
    model = Question


class RoundAdmin(admin.ModelAdmin):
    model = Question
    inlines = (QuestionInline,)
    actions = [reset, ]


admin.site.register(Round, RoundAdmin)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Bluff)
admin.site.register(Guess)
