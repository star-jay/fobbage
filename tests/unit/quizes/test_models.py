import pytest

from tests.factories.quiz_factories import (
    # QuizFactory,
    QuestionFactory,
    AnswerFactory,
    BluffFactory,
    FobbitFactory,
    SessionFactory,
)


@pytest.mark.django_db
def test_question_string_representation():
    """Make a clear string representation for the question"""
    question = QuestionFactory(text='test')

    assert question.__str__() == 'Question: test'


@pytest.mark.django_db
def test_answer_string_representation():
    """Make a clear string representation for the answer"""
    answer = AnswerFactory(
        order=1,
        fobbit__question__text='test',
    )

    assert answer.__str__() == 'test: Answer 1'


@pytest.mark.django_db
def test_bluff_string_representation():
    """Make a clear string representation for the bluff"""
    bluff = BluffFactory(
        player__first_name='otto',
        text='test',
    )

    assert bluff.__str__() == 'otto: test'


@pytest.mark.django_db
def test_multiplier():
    """Make a clear string representation for the bluff"""
    fobby = FobbitFactory(question__order=9)
    assert fobby.multiplier == 1
    fobby = FobbitFactory(question__order=10)
    assert fobby.multiplier == 1
    fobby = FobbitFactory(question__order=12)

    assert fobby.multiplier == 2
    fobby = FobbitFactory(question__order=22)

    assert fobby.multiplier == 3

    fobby = FobbitFactory(
        question__order=2,
        session=SessionFactory(settings={'questionsPerRound': 1}))
    assert fobby.multiplier == 2
