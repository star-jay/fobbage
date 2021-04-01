import random
from .models import Answer, Bluff, Guess, Fobbit


# create answers from
def generate_answers(fobbit_id):
    """
    Creates a new list of possible answers
    use a combination of bluffs and the correct answer
    """
    fobbit = Fobbit.objects.get(id=fobbit_id)
    if len(fobbit.session.players.all()) == 0:
        return False

    # Check if all players have bluffed
    if len(fobbit.bluffs.all()) != len(fobbit.session.players.all()):
        return False
    # Check if not already listed
    if fobbit.status >= Fobbit.GUESS:
        return False

    for answer in fobbit.answers.all():
        answer.delete()

    Answer.objects.create(
        fobbit=fobbit,
        text=fobbit.question.correct_answer,
        is_correct=True,
    )

    for bluff in fobbit.bluffs.all():
        answer = Answer.objects.filter(
            fobbit=fobbit,
            text__iexact=bluff.text).first()
        if answer is None:
            answer = Answer.objects.create(
                fobbit=fobbit,
                text=bluff.text)

        bluff.answer = answer
        bluff.save()

    answers = [answer for answer in fobbit.answers.all()]
    random.shuffle(answers)
    i = 0
    for answer in answers:
        answer.order = i = i + 1
        answer.save()

    fobbit.status = Fobbit.GUESS
    fobbit.save()
    return True


# SCORES
def score_for_session(player, session):
    score = 0
    for fobbit in session.fobbits.all():
        score += score_for_fobbit(player, fobbit)
    return score


def score_for_fobbit(player, fobbit):
    score = 0
    # only finnished questions have scores
    if fobbit.status != Fobbit.FINISHED:
        return 0

    player_bluff = fobbit.bluffs.filter(
        player=player,
        fobbit=fobbit).first()
    player_guess = Guess.objects.filter(
        answer__fobbit=fobbit,
        player=player).first()

    # als de speler heeft gebluffed
    if player_bluff:
        # 0 plunten als jouw bluff = correct antwoord
        if player_bluff.answer and player_bluff.answer.is_correct is True:
            return 0
        # 0 punten als je op je eigen antwoord stemt
        if player_guess.answer == player_bluff.answer:
            return 0

        score += player_bluff.score

    # score voor juist antwoord
    if player_guess:
        if player_guess.answer.text == fobbit.question.correct_answer:
            score += fobbit.multiplier * 1000

    return score


# SESSION
def next_question(session):
    questions = session.quiz.questions.exclude(
        id__in=[session.fobbits.values_list('question', flat=True)]
    )
    next = questions.first()

    fobbit = Fobbit.objects.create(
        question=next,
        session=session,
    )
    session.active_fobbit = fobbit
    session.save()
    return fobbit


# def prev_question_for_session(session):
#     active = session.active_fobbit
#     if active:
#         order = active.question.order
#         fobbit = session.fobbits.filter(
#             question__order=order-1).first()
#         if fobbit:
#             session.active_fobbit = fobbit
#             session.save()


# FOBBIT
def finish_fobbit(fobbit):
    """Finish the question if all players have guessed"""
    # TODO: Check if all players have guessed
    if len(fobbit.players_without_guess) == 0:
        fobbit.status = Fobbit.FINISHED
        fobbit.save()
    else:
        raise Guess.DoesNotExist("Not all players have guessed")


def reset_fobbit(fobbit):
    fobbit.status = Fobbit.BLUFF
    fobbit.bluffs.all().delete()
    fobbit.answers.all().delete()

    fobbit.save()


def hide_answers_for_fobbit(fobbit):
    if fobbit.status < Fobbit.FINISHED:
        # fobbit.guesses.delete()
        fobbit.answers.all().delete()

        fobbit.status = Fobbit.BLUFF
        fobbit.save()
        return True
