from django.contrib import admin

from .models import Quiz, Round, Question, Bluff


admin.site.register(Quiz)
admin.site.register(Round)
admin.site.register(Question)
admin.site.register(Bluff)
