from rest_framework import serializers
# from django.urls import reverse as django_reverse
# from rest_framework.reverse import reverse

from fobbage.accounts.serializers import UserSerializer
from fobbage.quizes.models import (
    Quiz, Question, Bluff, Answer, Guess, Fobbit, Session,
)
from fobbage.quizes.services import (
    score_for_bluff,
)


class BluffSerializer(serializers.ModelSerializer):
    player = UserSerializer()

    class Meta:
        model = Bluff
        fields = ('id', 'fobbit', 'player', 'text',)
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
    player = UserSerializer()

    class Meta:
        model = Guess
        fields = ('answer', 'player')

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


class ScoreSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    player = UserSerializer()

    def get_score(self, instance):
        return score_for_bluff(instance.player, instance)

    class Meta:
        model = Bluff
        fields = ('id', 'score', 'player')


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'text', 'fobbit', 'order')


class ScoreSheetSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True, source='bluffs', read_only=True)
    guesses = GuessSerializer(many=True,)

    class Meta:
        model = Answer
        fields = (
            'id', 'text', 'fobbit', 'order',
            'scores', 'guesses', 'is_correct',
        )


class QuestionSerializer(serializers.ModelSerializer):
    """Do not serialize the answer"""
    class Meta:
        model = Question
        fields = ('id', 'text', 'quiz')


class FobbitSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    score_sheets = ScoreSheetSerializer(
        many=True, read_only=True, source='scored_answers')

    bluffs = BluffSerializer(many=True, read_only=True)
    question = QuestionSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    have_bluffed = serializers.SerializerMethodField()
    have_guessed = serializers.SerializerMethodField()
    players_without_bluff = UserSerializer(
        many=True, read_only=True,
    )
    players_without_guess = UserSerializer(
        many=True, read_only=True,
    )

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
            'bluffs', 'question', 'answers', 'score_sheets',
            'players_without_bluff', 'players_without_guess',)


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
    fobbits = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    owner = UserSerializer()

    def get_fields(self):
        fields = super().get_fields()
        fields['active_fobbit'].queryset = Fobbit.objects.filter(
            session=self.instance)
        return fields

    def create(self, validated_data):
        if 'owner' not in validated_data:
            validated_data['owner'] = self.context['request'].user
            return super().create(validated_data)

    def get_websocket(self, instance):
        request = self.context.get('request', None)

        return '{}/ws/session/{}/'.format(
            request.get_host(),
            instance.id,
        )

    class Meta:
        read_only_fields = ['owner', ]
        model = Session
        fields = (
            'id',
            'url',
            'name',
            'websocket',
            'quiz',
            'owner',
            'active_fobbit',
            'fobbits',
        )


class ActiveFobbitSerializer(serializers.ModelSerializer):
    active_fobbit = serializers.PrimaryKeyRelatedField(
        queryset=Fobbit.objects.all()
    )

    def get_fields(self):
        fields = super().get_fields()
        fields['active_fobbit'].queryset = Fobbit.objects.filter(
            session=self.instance)
        return fields

    class Meta:
        model = Session
        fields = ('active_fobbit',)
