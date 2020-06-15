from django import forms
from django.core.validators import RegexValidator


from fobbage.quizes.models import Session, Quiz


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('name', 'quiz', 'players')


class NewQuizForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=100,
        # validators=[RegexValidator(
        #     '^(\\w+\\d+|\\d+\\w+)+$',
        #     message="Title should be a combination of letters and numbers"
        # )]
    )
