from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.db.models import Prefetch, Count
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    QuizSerializer, BluffSerializer, AnswerSerializer, SessionSerializer,
    GuessSerializer, FobbitSerializer, ActiveFobbitSerializer,
    QuestionSerializer, ScoreSerializer, RoundSerializer
)
from fobbage.quizes.models import (
    Quiz, Answer, Bluff, Guess, Session, Fobbit, Question)


# Get the UserModel
User = get_user_model()


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.filter(is_archived=False).prefetch_related(
        'players',
    ).select_related(
        'active_fobbit__question', 'owner',
    ).prefetch_related(
        Prefetch(
                'active_fobbit__answers',
                queryset=Answer.objects.prefetch_related(
                        'guesses',
                        'bluffs',
                        'bluffs__player',
                    ).annotate(
                        num_guesses=Count('guesses')
                    ).order_by('is_correct', 'num_guesses'),
                to_attr='scored_answers'
            ),
    )

    serializer_class = SessionSerializer

    @action(
        detail=True, methods=['POST'])
    def join(self, request, pk=None):
        session = self.get_object()
        user = request.user
        session.players.add(user)
        return Response(
            SessionSerializer(
                session,
                context=self.get_serializer_context()).data)

    @action(detail=True, methods=['POST'],)
    def next_question(self, request, pk=None):
        self.get_object().next_question()
        return Response(
            SessionSerializer(
                self.get_object(),
                context=self.get_serializer_context()).data)

    @action(detail=True, methods=['POST'], serializer_class=RoundSerializer)
    def new_round(self, request, pk=None):
        serializer = RoundSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.get_object().new_round(serializer.data)

        return Response(
            SessionSerializer(
                self.get_object(),
                context=self.get_serializer_context()).data)

    @action(
        detail=True, methods=['POST'], serializer_class=ActiveFobbitSerializer)
    def set_active_fobbit(self, request, pk=None):
        session = self.get_object()
        serializer = ActiveFobbitSerializer(
            instance=session, data=request.data)
        if serializer.is_valid():
            session = serializer.save()
            return Response(
                SessionSerializer(
                    session,
                    context=self.get_serializer_context()).data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['GET'])
    def score_board(self, request, pk=None):
        instance = self.get_object()

        return Response(
            ScoreSerializer(
                [
                    {
                        'score': instance.score_for_player(player),
                        'player': player
                    }
                    for player in instance.players.all()
                ],
                many=True
            ).data)


class FobbitViewSet(viewsets.ModelViewSet):
    serializer_class = FobbitSerializer


    def get_queryset(self):

        queryset = Fobbit.objects.all().select_related(
            'question', 'session',
        ).prefetch_related(
            Prefetch(
                'answers',
                queryset=Answer.objects.prefetch_related(
                        'guesses',
                        'bluffs',
                        'bluffs__player',
                    ),
            ),
            Prefetch(
                'answers',
                queryset=Answer.objects.prefetch_related(
                        'guesses',
                        'bluffs',
                        'bluffs__player',
                    ).annotate(
                        num_guesses=Count('guesses')
                    ).order_by('is_correct', 'num_guesses'),
                to_attr='scored_answers'
            ),)

        return queryset

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(
        detail=True, methods=['POST'],)
    def generate_answers(self, request, pk=None):
        fobbit = self.get_object()
        if fobbit.generate_answers():
            fobbit.session.next_question()
            return Response(
                FobbitSerializer(
                    fobbit, context=self.get_serializer_context()
                ).data)
        else:
            return Response(
                "Could not generate answers",
                status=status.HTTP_400_BAD_REQUEST, )

    @action(detail=True, methods=['POST'])
    def finish(self, request, pk=None, serializer_class=None):
        self.get_object().finish()
        return Response(
            FobbitSerializer(
                self.get_object(), context=self.get_serializer_context()
            ).data)

    @action(detail=True, methods=['POST'])
    def reset(self, request, pk=None):
        self.get_object().reset()
        return Response(
            FobbitSerializer(
                self.get_object(), context=self.get_serializer_context()
            ).data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ActiveFobbitViewSet(viewsets.ModelViewSet):
    serializer_class = FobbitSerializer

    def get_queryset(self):
        return Fobbit.objects.filter(
            session__in=Session.objects.values_list(
                'active_fobbit', flat=True))

    def retrieve(self, request, pk=None):
        fobbit = get_object_or_404(Session, id=pk).active_fobbit
        Session.objects.get(id=pk).active_fobbit
        serializer = FobbitSerializer(fobbit, context={'request': request})
        return Response(serializer.data)


class BluffViewSet(viewsets.ModelViewSet):
    serializer_class = BluffSerializer

    def get_queryset(self):
        if self.request.user:
            if self.request.user.is_superuser:
                return Bluff.objects.all()
            return Bluff.objects.filter(player=self.request.user)
        else:
            return Bluff.objects.none()

    def post(self, request, *args, **kwargs):
        return self.create(
            request, player=request.user, *args, **kwargs)


class GuessViewSet(viewsets.ModelViewSet):
    serializer_class = GuessSerializer

    def get_queryset(self):
        if self.request.user:
            return Guess.objects.filter(player=self.request.user)
        else:
            return Guess.objects.none()

    def post(self, request, *args, **kwargs):
        return self.create(
            request, player=request.user, *args, **kwargs)
