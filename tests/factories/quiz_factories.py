import factory

from fobbage.quizes.models import (
    Quiz, Round, Question, Answer, Bluff, Fobbit, Session
)
from tests.factories.account_factories import UserFactory


class QuizFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an example quiz """
    class Meta:
        model = Quiz

    # add a value for the required fields
    title = "factory quiz"
    created_by = factory.SubFactory(UserFactory)


class RoundFactory(factory.django.DjangoModelFactory):
    """ Factory that creates a round """
    class Meta:
        model = Round

    # add a value for the required fields
    quiz = factory.SubFactory(QuizFactory)
    title = factory.Sequence(lambda n: "round {}".format(n))
    multiplier = factory.Sequence(lambda n: n)


class QuestionFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an answer"""
    class Meta:
        model = Question

    # add a value for the required fields
    text = factory.Sequence(lambda n: "question {}".format(n))
    correct_answer = factory.Sequence(lambda n: "answer {}".format(n))
    round = factory.SubFactory(RoundFactory)
    order = factory.Sequence(lambda n: n)
    player = factory.SubFactory(UserFactory)


class SessionFactory(factory.django.DjangoModelFactory):
    """
    Factory for `Session`.
    """
    class Meta:
        model = Session
    # Example sequence field
    quiz = factory.SubFactory(QuizFactory)
    name = factory.Sequence(lambda n: 'Dummy Session: {}'.format(n))


class FobbitFactory(factory.django.DjangoModelFactory):
    """
    Factory for `Fobbit`.
    """
    class Meta:
        model = Fobbit
    # Example sequence field
    session = factory.SubFactory(SessionFactory)
    question = factory.SubFactory(QuestionFactory)


class AnswerFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an answer"""
    class Meta:
        model = Answer

    # add a value for the required fields
    text = factory.Sequence(lambda n: "answer {}".format(n))
    order = factory.Sequence(lambda n: n)
    fobbit = factory.SubFactory(FobbitFactory)


class BluffFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an bluff"""
    class Meta:
        model = Bluff

    # # add a value for the required fields
    # text = 'bluff'
    fobbit = factory.SubFactory(FobbitFactory)
    player = factory.SubFactory(UserFactory)
