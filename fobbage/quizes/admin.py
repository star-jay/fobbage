from django.contrib import admin

from .models import Quiz, Round, Question, Bluff, Guess


class QuestionInline(admin.TabularInline):
    model = Question


class RoundAdmin(admin.ModelAdmin):
    model = Question
    inlines = (QuestionInline,)


admin.site.register(Round, RoundAdmin)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Bluff)
admin.site.register(Guess)
