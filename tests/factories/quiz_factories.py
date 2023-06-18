import factory

from fobbage.quizes.models import (
    Quiz, Question, Answer, Bluff, Fobbit, Session, Guess,
)
from tests.factories.account_factories import UserFactory


class QuizFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an example quiz """
    class Meta:
        model = Quiz

    # add a value for the required fields
    title = "factory quiz"
    created_by = factory.SubFactory(UserFactory)


class QuestionFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an answer"""
    class Meta:
        model = Question

    # add a value for the required fields
    text = factory.Sequence(lambda n: "question {}".format(n))
    correct_answer = factory.Sequence(lambda n: "answer {}".format(n))
    quiz = factory.SubFactory(QuizFactory)
    order = factory.Sequence(lambda n: n)
    player = factory.SubFactory(UserFactory)


class SessionFactory(factory.django.DjangoModelFactory):
    """
    Factory for `Session`.
    """
    class Meta:
        model = Session
    # Example sequence field
    owner = factory.SubFactory(UserFactory)
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
    round = 1


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
    fobbit = factory.SubFactory(FobbitFactory)
    player = factory.SubFactory(UserFactory)
    text = factory.Sequence(lambda n: "bluff {}".format(n))


class GuessFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an Guess"""
    class Meta:
        model = Guess

    answer = factory.SubFactory(AnswerFactory)
    player = factory.SubFactory(UserFactory)
