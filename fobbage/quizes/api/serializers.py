from rest_framework import serializers
from django.urls import reverse as django_reverse
from rest_framework.reverse import reverse

from fobbage.quizes.models import (
    Quiz, Question, Bluff, Answer, Guess
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
    websocket = serializers.SerializerMethodField()

    def get_websocket(self, instance):
        request = self.context.get('request', None)
        if request.scheme == 'http':
            scheme = 'ws'
        else:
            scheme = 'wss'

        location = django_reverse(
            'room',
            args=(instance.id, ),
        )
        # location = django_reverse(
        #      'room',
        #     args=(instance.id, ),
        #     request=request,
        # )

        return '{}/ws{}'.format(
            scheme,
            request.get_host(),
            location,
        )

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
            'websocket',
        )
