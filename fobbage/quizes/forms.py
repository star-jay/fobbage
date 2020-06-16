from django import forms
from fobbage.quizes.models import Session, Bluff


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('quiz', 'name', 'players')


class BluffForm(forms.ModelForm):
    text = forms.Textarea()

    class Meta:
        model = Bluff
        fields = ('text',)
        # fields = ('text', 'player', 'fobbit')
        exclude = ('player', 'fobbit')


class NewQuizForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=100,
    )
