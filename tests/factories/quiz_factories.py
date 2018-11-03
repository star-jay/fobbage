import factory

from fobbage.quizes.models import (
    Quiz,
)


class QuizFactory(factory.Factory):
    """ Factory that creates an example quiz """
    class Meta:
        model = Quiz

    # add a value for the required fields
    title = "factory quiz"