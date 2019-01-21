from rest_framework import serializers
from fobbage.quizes.models import (
    Quiz, Round, Question
)


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'text', 'status')


class QuizSerializer(serializers.ModelSerializer):

    active_question = serializers.SerializerMethodField()

    def get_active_question(self, quiz):
        active_round = quiz.rounds.get(is_active=True)
        if active_round:
            return QuestionSerializer(
                active_round.questions.get(
                    status__in=[Question.BLUFF, Question.GUESS])
            ).data
        return None

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'active_question',
        )
