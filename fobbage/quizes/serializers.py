from rest_framework import serializers
from django.urls import reverse as django_reverse
# from rest_framework.reverse import reverse

from fobbage.quizes.models import (
    Quiz, Question, Bluff, Answer, Guess
)


class BluffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bluff
        fields = ('id', 'text', 'question', 'player')
        extra_kwargs = {
            'text': {'write_only': True},
            'player': {'read_only': True},
        }

    # overrride create to save user
    def create(self, validated_data):
        question = self.validated_data['question']
        user = self.context['request'].user

        if user not in question.round.quiz.players.all():
            raise serializers.ValidationError(
                'player is not playing this quiz')

        validated_data['player'] = user

        if Bluff.objects.filter(
            player=validated_data['player'],
            question=validated_data['question'],
        ).count() > 0:
            raise serializers.ValidationError(
                'player already bluffed for this question')
        return Bluff.objects.create(**validated_data)


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ('answer', )

    # overide create to save user
    def create(self, validated_data):
        validated_data['player'] = self.context['request'].user
        answer = Answer.objects.filter(
            id=validated_data['answer'].id
        ).first()
        if answer:
            if Guess.objects.filter(
                player=validated_data['player'],
                answer__question=answer.question,
            ).count() > 0:
                raise serializers.ValidationError
            return Guess.objects.create(**validated_data)

        raise serializers.ValidationError


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'question', 'order')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'status', 'answers')


class QuizSerializer(serializers.ModelSerializer):
    websocket = serializers.SerializerMethodField()

    def get_websocket(self, instance):
        request = self.context.get('request', None)

        return '{}/ws/quiz/{}/'.format(
            request.get_host(),
            instance.id,
        )

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'websocket',
        )
