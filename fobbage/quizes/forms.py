from django import forms
from django.core.validators import RegexValidator


class NewQuizForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=100,
        validators=[RegexValidator(
            '^(\\w+\\d+|\\d+\\w+)+$',
            message="Title should be a combination of letters and numbers"
        )])
