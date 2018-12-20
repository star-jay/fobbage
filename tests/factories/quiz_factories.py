import factory

from fobbage.quizes.models import (
    Quiz, Round, Question, Answer, Bluff
)
from tests.factories.account_factories import UserFactory


class QuizFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an example quiz """
    class Meta:
        model = Quiz

    # add a value for the required fields
    title = "factory quiz"


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


class AnswerFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an answer"""
    class Meta:
        model = Answer

    # add a value for the required fields
    text = factory.Sequence(lambda n: "answer {}".format(n))
    order = factory.Sequence(lambda n: n)
    question = factory.SubFactory(QuestionFactory)


class BluffFactory(factory.django.DjangoModelFactory):
    """ Factory that creates an bluff"""
    class Meta:
        model = Bluff

    # # add a value for the required fields
    # text = 'bluff'
    question = factory.SubFactory(QuestionFactory)
    player = factory.SubFactory(UserFactory)
