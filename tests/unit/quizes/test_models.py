import pytest

from tests.factories.quiz_factories import (
    QuizFactory,
    RoundFactory,
    QuestionFactory,
    AnswerFactory,
    BluffFactory,
)


@pytest.mark.django_db
def test_quiz_string_representation():
    """Make a clear string representation for the quiz"""
    quiz = QuizFactory(title='test')

    assert quiz.__str__() == 'Quiz: test'


@pytest.mark.django_db
def test_round_string_representation():
    """Make a clear string representation for the round"""
    obj = RoundFactory(title='test')

    assert obj.__str__() == 'Round: test'


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
