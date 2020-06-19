import random
from .models import Answer, Bluff, Guess, Fobbit


# create answers from
def generate_answers(fobbit_id):
    """
    Creates a new list of possible answers
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

        score += score_for_bluff(player, player_bluff)

    # score voor juist antwoord
    if player_guess:
        if player_guess.answer.text == fobbit.question.correct_answer:
            score += fobbit.multiplier * 1000

    return score


def score_for_bluff(player, bluff):
    score = 0

    player_guess = Guess.objects.filter(
        answer__fobbit=bluff.fobbit,
        player=player).first()

    # 0 plunten als jouw bluff = correct antwoord
    if bluff.answer and bluff.answer.is_correct is True:
        return 0
    # 0 punten als je op je eigen antwoord stemtgit
    if player_guess.answer == bluff.answer:
        return 0

    # score voor anders spelers kiezen jouw bluff
    aantal_gepakt = len(Guess.objects.filter(answer=bluff.answer))

    score += (aantal_gepakt * bluff.fobbit.multiplier * 500) / len(
        Bluff.objects.filter(answer=bluff.answer))

    return score
