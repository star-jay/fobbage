import pytest

from tests.factories.quiz_factories import (
    # QuizFactory,
    # RoundFactory,
    QuestionFactory,
    # AnswerFactory,
    BluffFactory,
)

from fobbage.quizes.services import generate_answers
from fobbage.quizes.models import Question


@pytest.mark.django_db
def test_question_generate_answers():
    bluff = BluffFactory(question__status=Question.BLUFF)
    bluff.question.round.quiz.players.set(
        [bluff.player])

    assert generate_answers(bluff.question.id)

    assert len(bluff.question.answers.all()) == 2


@pytest.mark.django_db
def test_answers_group_unique():
    question = QuestionFactory(status=Question.BLUFF)
    bluff = BluffFactory(question=question)
    bluff2 = BluffFactory(question=question, text=bluff.text)

    question.round.quiz.players.set(
        [bluff.player, bluff2.player])

    assert generate_answers(bluff.question.id)

    assert len(bluff.question.answers.all()) == 2
