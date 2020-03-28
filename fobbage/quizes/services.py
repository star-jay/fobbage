import random
from .models import Question, Answer, Bluff, Guess, Fobbit


# create answers from
def generate_answers(fobbit_id):
    """
    Create's a new list of possible answers
    use a combination of bluffs and the correct answer
    """
    fobbit = Fobbit.objects.get(id=fobbit_id)

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
        score += score_for_fobbit(player, round)
    return score


def score_for_round(player, round):
    score = 0
    for question in round.questions.all():
        score += score_for_question(player, question)
    return score


def score_for_question(player, question):
    score = 0
    # only finnished questions have scores
    if question.status != Question.FINISHED:
        return 0

    player_bluff = question.bluffs.filter(
        player=player,
        question=question).first()
    player_guess = Guess.objects.filter(
        answer__question=question,
        player=player).first()

    # 0 plunten als jouw bluff = correct antwoord
    if player_bluff.answer.is_correct is True:
        return 0
    # 0 punten als je op je eigen antwoord stemt
    if player_guess.answer == player_bluff.answer:
        return 0

    # score voor juist antwoord
    if player_guess.answer.text == question.correct_answer:
        score += question.round.multiplier * 1000

    score += score_for_bluff(player, player_bluff)

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

    # 0 plunten als jouw bluff = correct antwoord
    if player_bluff.answer.is_correct is True:
        return 0
    # 0 punten als je op je eigen antwoord stemt
    if player_guess.answer == player_bluff.answer:
        return 0

    # score voor juist antwoord
    if player_guess.answer.text == fobbit.correct_answer:
        score += fobbit.round.multiplier * 1000

    score += score_for_bluff(player, player_bluff)

    return score


def score_for_bluff(player, bluff):
    score = 0

    player_guess = Guess.objects.filter(
        answer__fobbit=bluff.fobbit,
        player=player).first()

    # 0 plunten als jouw bluff = correct antwoord
    if bluff.answer.is_correct is True:
        return 0
    # 0 punten als je op je eigen antwoord stemtgit
    if player_guess.answer == bluff.answer:
        return 0

    # score voor anders spelers kiezen jouw bluff
    aantal_gepakt = len(Guess.objects.filter(answer=bluff.answer))

    score += (aantal_gepakt * bluff.fobbit.round.multiplier * 500) / len(
        Bluff.objects.filter(answer=bluff.answer))

    return score
