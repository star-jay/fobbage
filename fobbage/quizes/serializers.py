from rest_framework import serializers
# from django.urls import reverse as django_reverse
# from rest_framework.reverse import reverse

from fobbage.quizes.models import (
    Quiz, Question, Bluff, Answer, Guess,
)


class BluffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bluff
        fields = ('id', 'text', 'fobbit', 'player')
        extra_kwargs = {
            # 'text': {'write_only': True},
            'player': {'read_only': True},
        }

    # override create to save user
    def create(self, validated_data):
        question = self.validated_data['question']
        user = self.context['request'].user

        if user not in question.quiz.players.all():
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
                raise serializers.ValidationError(
                    'you already made a guess for this question')
            return Guess.objects.create(**validated_data)

        raise serializers.ValidationError


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'fobbit', 'order')


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'text', 'quiz')


class FobbitSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    have_bluffed = serializers.SerializerMethodField()
    have_guessed = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    modus = serializers.SerializerMethodField()

    def get_modus(self, instance):
        return instance.session.modus

    def get_text(self, instance):
        return instance.question.text

    def get_have_bluffed(self, instance):
        player = self.context['request'].user
        return Bluff.objects.filter(
            player=player, question=instance.id).count() > 0

    def get_have_guessed(self, instance):
        player = self.context['request'].user
        return Guess.objects.filter(
            player=player, answer__question=instance.id).count() > 0

    class Meta:
        model = Question
        fields = (
            'id', 'text', 'status', 'answers', 'have_bluffed', 'have_guessed',
            'modus')


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
