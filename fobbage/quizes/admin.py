from django.contrib import admin

from .models import Quiz, Round, Question, Bluff


class QuestionInline(admin.TabularInline):
    model = Question


class RoundAdmin(admin.ModelAdmin):
    model = Question
    inlines = (QuestionInline,)


admin.site.register(Round, RoundAdmin)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Bluff)
