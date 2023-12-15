from rest_framework import serializers
# from django.urls import reverse as django_reverse
# from rest_framework.reverse import reverse

from fobbage.accounts.serializers import UserSerializer
from fobbage.quizes.models import (
    Quiz, Question, Bluff, Answer, Guess, Fobbit, Session,
)


class RoundSerializer(serializers.Serializer):
    multiplier = serializers.IntegerField()
    number_of_questions = serializers.IntegerField()


class BluffSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)

    class Meta:
        model = Bluff
        fields = ('id', 'fobbit', 'player', 'text',)
        extra_kwargs = {
            'player': {'read_only': True},
        }

    def validate(self, attrs):
        fobbit = attrs['fobbit']
        user = self.context['request'].user

        if user not in fobbit.session.players.all():
            raise serializers.ValidationError(
                'player is not playing this session')

        attrs['player'] = user

        return super().validate(attrs)

    # Override create to save user
    def create(self, validated_data):
        if Bluff.objects.filter(
            player=validated_data['player'],
            fobbit=validated_data['fobbit'],
        ).count() > 0:
            raise serializers.ValidationError(
                'player already bluffed for this question')
        return Bluff.objects.create(**validated_data)


class GuessSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)
    score = serializers.IntegerField(read_only=True)

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

    class Meta:
        model = Guess
        fields = ('answer', 'player', 'score')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'fobbit', 'order')


class ScoreSerializer(serializers.Serializer):
    # Serialize a single score for each bluff in an answer
    score = serializers.IntegerField()
    player = UserSerializer()


class AnswerScoreSheetSerializer(serializers.ModelSerializer):
    scores = serializers.SerializerMethodField()
    guesses = GuessSerializer(many=True,)

    def get_scores(self, instance):
        return ScoreSerializer(
            [
                {
                    'score': bluff.score,
                    'player': bluff.player
                }
                for bluff in instance.bluffs.all()
            ],
            many=True
        ).data

    class Meta:
        model = Answer
        fields = (
            'id', 'text', 'order',
            'scores', 'guesses', 'is_correct',
        )


class QuestionSerializer(serializers.ModelSerializer):
    """Do not serialize the answer"""
    image_url = serializers.CharField()

    class Meta:
        model = Question
        fields = ('id', 'text', 'url', 'quiz', 'image_url', 'order')


class FobbitSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    score_sheets = AnswerScoreSheetSerializer(
        many=True, read_only=True, source='scored_answers')

    # bluffs = BluffSerializer(many=True, read_only=True)
    question = QuestionSerializer(read_only=True)
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
            'status',
            'have_bluffed',
            'have_guessed',
            'question',
            'answers',
            'score_sheets',
            'players_without_bluff',
            'players_without_guess',
            'session', 'multiplier'
        )


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
    owner = UserSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        return fields

    def create(self, validated_data):
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
            'settings',
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
