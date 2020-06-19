from django import forms
from fobbage.quizes.models import Session, Bluff, Guess


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
        # exclude = ('player', 'fobbit')


class GuessForm(forms.ModelForm):
    # answer = forms.ChoiceField()

    class Meta:
        model = Guess
        fields = ('answer',)


class NewQuizForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=100,
    )
