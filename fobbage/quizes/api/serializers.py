from rest_framework import serializers
from fobbage.quizes.models import (
    Quiz, Round, Question, Bluff, Answer, Guess
)


class BluffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bluff
        fields = ('text', 'question')

    # overrride create to save user
    def create(self, validated_data):
        # question = self.validated_data['question']
        # question = Question.objects.filter(id=question)

        # if self.context['request'].user not in question.round.quiz.players:
        #     raise serializers.ValidationError

        validated_data['player'] = self.context['request'].user

        if Bluff.objects.filter(
            player=validated_data['player'],
            question=validated_data['question'],
        ).count() > 0:
            raise serializers.ValidationError
        return Bluff.objects.create(**validated_data)


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ('answer', )

    # overide create to save user
    def create(self, validated_data):
        validated_data['player'] = self.context['request'].user
        if Guess.objects.filter(
            player=validated_data['player'],
            answer=validated_data['answer'],
        ).count() > 0:
            raise serializers.ValidationError
        return Guess.objects.create(**validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'question', 'order')


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self, instance):
        if instance.status >= Question.GUESS:
            return AnswerSerializer(
                instance.answers, many=True).data
        return None

    class Meta:
        model = Question
        fields = ('id', 'text', 'status', 'answers')


class QuizSerializer(serializers.ModelSerializer):

    active_question = serializers.SerializerMethodField()

    def get_active_question(self, quiz):
        # active_round = quiz.rounds.get(is_active=True)
        if quiz.active_round and quiz.active_round.active_question:
            return QuestionSerializer(
                Question.objects.get(
                    id=quiz.active_round.active_question)
            ).data
        return None

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'active_question',
        )
