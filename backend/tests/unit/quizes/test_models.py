import pytest

from tests.factories.quiz_factories import (
    # QuizFactory,
    QuestionFactory,
    AnswerFactory,
    BluffFactory,
    FobbitFactory,
    SessionFactory,
    UserFactory,
    GuessFactory,
    Fobbit,
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


@pytest.mark.django_db
def test_scores_new_player():
    rounds = [
        dict(multiplier=1),
        dict(multiplier=5),
    ]

    session = SessionFactory(settings={'rounds': rounds})

    BluffFactory(fobbit__session=session)
    BluffFactory(fobbit__session=session)
    GuessFactory(answer__fobbit__session=session)

    new_player = UserFactory()
    session.players.add(new_player)

    assert session.score_for_player(new_player) == 0, "A new player has no score"  # noqa


@pytest.mark.django_db
def test_scores_fobbit_random_player():
    fobbit = FobbitFactory(status=Fobbit.FINISHED)

    new_player = UserFactory()
    assert fobbit.score_for_player(new_player) == 0, "A new player has no score"  # noqa


@pytest.mark.django_db
def test_generate_answers():
    session = SessionFactory()
    fobbit = FobbitFactory(session=session, question__text='foo')

    player1 = UserFactory()
    player2 = UserFactory()

    session.players.add(player1, player2)

    BluffFactory(fobbit=fobbit, player=player1, text='bar')
    BluffFactory(fobbit=fobbit, player=player2, text='bib')

    fobbit.generate_answers()

    assert fobbit.answers.count() == 3


@pytest.mark.django_db
def test_test_scores():
    session = SessionFactory()
    fobbit = FobbitFactory(session=session, question__text='foo')

    player1 = UserFactory()
    player2 = UserFactory()

    session.players.add(player1, player2)

    BluffFactory(fobbit=fobbit, player=player1, text='bar')
    bluff2 = BluffFactory(fobbit=fobbit, player=player2, text='bib')

    fobbit.generate_answers()

    assert fobbit.answers.count() == 3
    bluff2.refresh_from_db()

    fobbit.status = Fobbit.FINISHED
    fobbit.save()

    GuessFactory(
        answer=bluff2.answer,
        player=player1)

    assert bluff2.score == 500


@pytest.mark.django_db
def test_test_scores_correct():
    session = SessionFactory()
    fobbit = FobbitFactory(session=session, question__text='foo')

    player1 = UserFactory()
    player2 = UserFactory()

    session.players.add(player1, player2)

    BluffFactory(fobbit=fobbit, player=player1, text='bar')
    BluffFactory(fobbit=fobbit, player=player2, text='bib')

    fobbit.generate_answers()

    assert fobbit.answers.count() == 3

    fobbit.status = Fobbit.FINISHED
    fobbit.save()

    GuessFactory(
        answer=fobbit.answers.filter(bluffs__player=player2).first(),
        player=player1)

    GuessFactory(
        answer=fobbit.answers.filter(bluffs__player__isnull=True).first(),
        player=player2)

    assert fobbit.score_for_player(player2) == 1500


@pytest.mark.django_db
def test_session_scores_correct():
    session = SessionFactory()
    fobbit = FobbitFactory(session=session, question__text='foo')

    player1 = UserFactory()
    player2 = UserFactory()

    session.players.add(player1, player2)

    BluffFactory(fobbit=fobbit, player=player1, text='bar')
    BluffFactory(fobbit=fobbit, player=player2, text='bib')

    fobbit.generate_answers()

    assert fobbit.answers.count() == 3
    GuessFactory(
            answer=fobbit.answers.filter(bluffs__player=player2).first(),
            player=player1)
    GuessFactory(
        answer=fobbit.answers.filter(bluffs__player__isnull=True).first(),
        player=player2)

    fobbit.finish()

    assert session.score_for_player(player2) == 1500
