import pytest

from tests.factories.quiz_factories import (
    # QuizFactory,
    # RoundFactory,
    # QuestionFactory,
    # AnswerFactory,
    BluffFactory,
    FobbitFactory,
)

from fobbage.quizes.services import generate_answers
from fobbage.quizes.models import Fobbit


@pytest.mark.django_db
def test_question_generate_answers():
    bluff = BluffFactory(fobbit__status=Fobbit.BLUFF)
    bluff.fobbit.session.players.set(
        [bluff.player])

    assert generate_answers(bluff.fobbit.id)

    assert len(bluff.fobbit.answers.all()) == 2


@pytest.mark.django_db
def test_answers_group_unique():
    fobbit = FobbitFactory(status=Fobbit.BLUFF)
    bluff = BluffFactory(fobbit=fobbit)
    bluff2 = BluffFactory(fobbit=fobbit, text=bluff.text)

    fobbit.session.players.set(
        [bluff.player, bluff2.player])

    assert generate_answers(bluff.fobbit.id)

    assert len(bluff.fobbit.answers.all()) == 2
