from rest_framework import serializers
# from django.urls import reverse as django_reverse
# from rest_framework.reverse import reverse

from fobbage.quizes.models import (
    Quiz, Question, Bluff, Answer, Guess, Fobbit, Session,
)
from fobbage.quizes.services import (
    # generate_answers,
    # score_for_session,
    # score_for_bluff,
    next_question_for_session,
    # prev_question_for_session,
    finish_fobbit,
    reset_fobbit,
)


class BluffSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='player.username', read_only=True)

    class Meta:
        model = Bluff
        fields = ('id', 'question', 'player', 'username', 'text',)
        extra_kwargs = {
            'player': {'read_only': True},
        }

    # Override create to save user
    def create(self, validated_data):
        fobbit = self.validated_data['fobbit']
        user = self.context['request'].user

        if user not in fobbit.session.players.all():
            raise serializers.ValidationError(
                'player is not playing this session')

        validated_data['player'] = user

        if Bluff.objects.filter(
            player=validated_data['player'],
            fobbit=validated_data['fobbit'],
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
                answer__fobbit=answer.fobbit,
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
    """Do not serialize the answer"""
    class Meta:
        model = Question
        fields = ('id', 'text', 'quiz')


class FobbitSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    bluffs = BluffSerializer(many=True, read_only=True)
    question = QuestionSerializer(read_only=True)
    have_bluffed = serializers.SerializerMethodField()
    have_guessed = serializers.SerializerMethodField()

    def get_have_bluffed(self, instance):
        if 'request' in self.context:
            player = self.context['request'].user
            return Bluff.objects.filter(
                player=player, fobbit=instance.id).count() > 0

    def get_have_guessed(self, instance):
        if 'request' in self.context:
            player = self.context['request'].user
            return Guess.objects.filter(
                player=player, answer__fobbit=instance.id).count() > 0

    class Meta:
        model = Fobbit
        fields = (
            'id',
            'url',
            'status', 'have_bluffed', 'have_guessed',
            'bluffs', 'question', 'answers')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
        )


class SessionSerializer(serializers.ModelSerializer):
    websocket = serializers.SerializerMethodField()
    active_fobbit = FobbitSerializer(read_only=True)
    # questions = serializers.SerializerMethodField()

    # def get_questions(self, instance):
    #     return QuestionSerializer(
    #         Question.objects.filter(quiz=instance.quiz), many=True).data

    def get_websocket(self, instance):
        request = self.context.get('request', None)

        return '{}/ws/session/{}/'.format(
            request.get_host(),
            instance.id,
        )

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'name',
            'websocket',
            'quiz',
            'owner',
            'active_fobbit',
            # 'questions'
        )

    # generate_answers, score_for_session, score_for_bluff,
    # next_question_for_session, prev_question_for_session,


class FinishFobbitSerializer(serializers.Serializer):
    # fobbit = serializers.PrimaryKeyRelatedField(
    #     queryset=Fobbit.objects.all(),
    # )

    def save(self):
        finish_fobbit(self.instance)
        return self.instance


class ResetFobbitSerializer(serializers.Serializer):
    # fobbit = serializers.PrimaryKeyRelatedField(
    #     queryset=Fobbit.objects.all(),
    # )

    def save(self):
        reset_fobbit(self.instance)
        return self.instance


class NextQuestionSerializer(serializers.Serializer):

    def save(self):
        next_question_for_session(self.instance)
        return self.instance
