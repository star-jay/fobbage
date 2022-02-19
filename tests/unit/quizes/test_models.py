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
    # get multiplier from round
    rounds = [
        dict(multiplier=1),
        dict(multiplier=5),
    ]

    session = SessionFactory(settings={'rounds': rounds})

    fobby = FobbitFactory(
        session=session,
        round=0,
    )
    assert fobby.multiplier == 1
    fobby = FobbitFactory(
        session=session,
        round=1,
    )
    assert fobby.multiplier == 5

    # default = round +1
    fobby = FobbitFactory(
        session=session,
        round=2,
    )
    assert fobby.multiplier == 3


@pytest.mark.django_db
def test_new_round():
    # test new round create new fibby
    rounds = [
        dict(multiplier=1),
        dict(multiplier=5),
    ]

    session = SessionFactory(settings={'rounds': rounds})

    q1 = QuestionFactory(quiz=session.quiz)
    QuestionFactory(quiz=session.quiz)
    q3 = QuestionFactory(quiz=session.quiz)

    session.new_round({'multiplier': 1, 'number_of_questions': 3})
    assert session.active_fobbit.question == q1

    session.next_question()
    session.next_question()
    assert session.active_fobbit.question == q3
    session.next_question()

    assert session.modus == 1
    assert session.active_fobbit.question == q1
