import random
from .models import Question, Answer, Bluff, Guess


# create answers from
def generate_answers(question_id):
    """
    Create's a new list of possible answers
    use a combination of bluffs and the correct answer
    """
    question = Question.objects.get(id=question_id)

    # Check if all players have bluffed
    if len(question.bluffs.all()) != len(question.round.quiz.players.all()):
        return False
    # Check if not already listed
    if question.status >= Question.GUESS:
        return False

    for answer in question.answers.all():
        answer.delete()

    Answer.objects.create(
        question=question,
        text=question.correct_answer,
        is_correct=True,
    )

    for bluff in question.bluffs.all():
        answer = Answer.objects.filter(
            question=question,
            text__iexact=bluff.text).first()
        if answer is None:
            answer = Answer.objects.create(
                question=question,
                text=bluff.text)

        bluff.answer = answer
        bluff.save()

    answers = [answer for answer in question.answers.all()]
    random.shuffle(answers)
    i = 0
    for answer in answers:
        answer.order = i = i + 1
        answer.save()

    question.status = Question.GUESS
    question.save()
    return True


# SCORES
def score_for_quiz(player, quiz):
    score = 0
    for round in quiz.rounds.all():
        score += score_for_round(player, round)
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


def score_for_bluff(player, bluff):
    score = 0

    player_guess = Guess.objects.filter(
        answer__question=bluff.question,
        player=player).first()

    # 0 plunten als jouw bluff = correct antwoord
    if bluff.answer.is_correct is True:
        return 0
    # 0 punten als je op je eigen antwoord stemtgit
    if player_guess.answer == bluff.answer:
        return 0

    # score voor anders spelers kiezen jouw bluff
    aantal_gepakt = len(Guess.objects.filter(answer=bluff.answer))

    score += (aantal_gepakt * bluff.question.round.multiplier * 500) / len(
        Bluff.objects.filter(answer=bluff.answer))

    return score
