import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.views.generic import DetailView, ListView, CreateView
# from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import (
    QuizSerializer, BluffSerializer, AnswerSerializer, SessionSerializer,
    GuessSerializer, QuestionSerializer, FobbitSerializer,)
from .services import (
    generate_answers, score_for_session, score_for_bluff, )
from fobbage.quizes.models import (
    Quiz, Question, Answer, Bluff, Guess, Session, Fobbit)

from .forms import (
    NewQuizForm, SessionForm, BluffForm, GuessForm,
    SessionUpdateForm, )

from django.contrib.auth import get_user_model

# Get the UserModel
User = get_user_model()


def new_quiz(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewQuizForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            quiz = Quiz.objects.create(
                title=form.cleaned_data['title'],
                created_by=request.user)

            # redirect to a new URL:
            return HttpResponseRedirect('/chat/{}/'.format(quiz.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewQuizForm()

    return render(request, 'quizes/new.html', {'form': form})


def index(request):
    return render(request, 'quizes/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def quiz_view(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    context = {
        'quiz': quiz,
    }

    return render(
        request, 'quizes/quiz.html', context)


def session_view(request, session_id):
    session = Session.objects.get(pk=session_id)
    context = {
        'session': session,
    }
    fobbit = session.active_fobbit
    context['fobbit'] = fobbit

    if fobbit:
        players = None
        if fobbit.status == Fobbit.BLUFF:
            players = fobbit.players_without_bluff()
        elif fobbit.status == Fobbit.GUESS:
            players = fobbit.players_without_guess()

        if players:
            context['players'] = players
        else:
            context['players'] = session.players.all()

    return render(
        request, 'quizes/session.html', context)


def session_join(request, session_id):
    session = Session.objects.get(pk=session_id)
    session.players.add(request.user)
    session.save()

    return HttpResponseRedirect(f'/session/{session.id}/play')


def session_play(request, session_id):
    session = Session.objects.get(pk=session_id)
    context = {
            'session': session,
            'fobbit': session.active_fobbit,
        }

    if session.modus == Session.BLUFFING:
        bluff = Bluff.objects.filter(
            fobbit=session.active_fobbit,
            player=request.user,
        ).first()
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            data = request.POST.copy()
            data['player'] = request.user,
            data['fobbit'] = session.active_fobbit
            # create a form instance
            # and populate it with data from the request:
            form = BluffForm(data, instance=bluff)
            # check whether it's valid:
            if form.is_valid():
                bluff = form.save(commit=False)
                bluff.player = request.user
                bluff.fobbit = session.active_fobbit
                bluff.save()
                return HttpResponseRedirect(f'/session/{session.id}/play')
            else:
                context['form'] = BluffForm(data)
        else:
            context['bluff'] = bluff
            context['form'] = BluffForm(instance=bluff)

        return render(
            request, 'quizes/bluff.html', context)

    if session.modus == Session.GUESSING:
        guess = Guess.objects.filter(
            answer__fobbit=session.active_fobbit,
            player=request.user,
        ).first()
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            data = request.POST.copy()
            data['player'] = request.user.id,
            data['fobbit'] = session.active_fobbit
            # create a form instance
            # and populate it with data from the request:
            form = GuessForm(data, instance=guess)
            # check whether it's valid:
            if form.is_valid():
                guess = form.save(commit=False)
                guess.player = request.user
                guess.fobbit = session.active_fobbit
                guess.save()

                return HttpResponseRedirect(f'/session/{session.id}/play')
            else:
                context['form'] = GuessForm(data)
                answers = Answer.objects.filter(
                    fobbit=session.active_fobbit,)
                context['form'].fields["answer"].queryset = answers

        else:
            context['guess'] = guess
            context['form'] = GuessForm(instance=guess)
            answers = Answer.objects.filter(
                fobbit=session.active_fobbit,)
            context['form'].fields["answer"].queryset = answers

        return render(
            request, 'quizes/guess.html', context)


def next_question(self, session_id):
    session = Session.objects.get(id=session_id)
    session.next_question()
    return HttpResponseRedirect(
        reverse('session', args=(session.id,)))


def prev_question(self, session_id):
    session = Session.objects.get(id=session_id)
    session.prev_question()
    return HttpResponseRedirect(
        reverse('session', args=(session.id,)))


def collect_answers(request, fobbit_id):
    fobbit = Fobbit.objects.get(pk=fobbit_id)
    generate_answers(fobbit.id)

    return HttpResponseRedirect(
        reverse('session', args=(fobbit.session.id,)))


def reset_fobbit(request, fobbit_id):
    fobbit = Fobbit.objects.get(pk=fobbit_id)
    fobbit.reset()

    return HttpResponseRedirect(
        reverse('session', args=(fobbit.session.id,)))


def hide_answers(request, fobbit_id):
    fobbit = Fobbit.objects.get(pk=fobbit_id)
    fobbit.hide_answers()

    return HttpResponseRedirect(
        reverse('session', args=(fobbit.session.id,)))


def start_guessing(request, session_id):
    session = Session.objects.get(pk=session_id)
    session.modus = Session.GUESSING
    session.save()

    return HttpResponseRedirect(
        reverse('session', args=(session.id,)))


def start_bluffing(request, session_id):
    session = Session.objects.get(pk=session_id)
    session.modus = Session.BLUFFING
    session.save()

    return HttpResponseRedirect(
        reverse('session', args=(session.id,)))


def show_scores(request, fobbit_id):
    fobbit = Fobbit.objects.get(pk=fobbit_id)
    if fobbit.finish():
        # show player answers
        answer = Answer.objects \
            .filter(
                fobbit=fobbit,
                showed=False,
                is_correct=False) \
            .annotate(num_guesses=Count('guesses')) \
            .order_by('num_guesses') \
            .first()
        if answer:
            answer.showed = True
            answer.save()
        else:
            # reset answers to show again
            Answer.objects.filter(
                fobbit=fobbit).update(
                    showed=False)
            # show correct answer
            answer = Answer.objects.filter(
                fobbit=fobbit,
                is_correct=True).get()

        if answer:
            # bluffs en scores
            if len(answer.bluffs.all()) > 0:
                bluffs = [
                    {
                        'player': bluff.player,
                        'score': score_for_bluff(bluff.player, bluff)
                    } for bluff in answer.bluffs.all()
                ]
            else:
                bluffs = None
            # show the answer

            context = {
                'answer': answer,
                'bluffs': bluffs}
            return render(
                request, 'quizes/scores.html', context)

    return HttpResponseRedirect(
        reverse('session', args=(fobbit.session.id,)))


def scoreboard(request, session_id):
    session = Session.objects.get(pk=session_id)
    active_fobbit = session.active_fobbit
    scores = {
        player: score_for_session(player, session)
        for player in session.players.all()
    }
    ranking = sorted(scores, key=scores.__getitem__, reverse=True)
    ranked_scores = [(player, scores[player]) for player in ranking]
    context = {
        'scores': ranked_scores,
        'active_fobbit': active_fobbit,
        'session': session,
    }
    return render(
        request, 'quizes/leaderboard.html', context)


class QuizDetail(DetailView):
    template_name = 'quizes/quiz_detail.html'
    model = Quiz

    def get_queryset(self):
        if self.request.user:
            return Quiz.objects.filter(created_by=self.request.user)
        else:
            return Quiz.objects.none()


class QuizList(ListView):
    template_name = 'quizes/quiz_list.html'
    model = Quiz

    def get_queryset(self):
        if self.request.user:
            return Quiz.objects.filter(created_by=self.request.user)
        else:
            return Quiz.objects.none()


class SessionList(ListView):
    mode = 'list'
    template_name = 'quizes/session_list.html'
    model = Session
    queryset = Session.objects.all()

    def get_context_data(self, **kwargs):
        """add the mode"""
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['mode'] = "join"
        return context


class SessionJoin(SessionList):
    pass


class SessionContinue(SessionList):

    def get_queryset(self):
        return Session.objects.filter(
            owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['mode'] = "continue"
        return context


class SessionCreateView(CreateView):
    model = Session
    form_class = SessionForm

    def form_valid(self, form):
        session = form.save(commit=False)
        session.owner = self.request.user
        session.save()
        self.object = session

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('session', kwargs={'session_id': self.object.id})


class SessionUpdate(CreateView):
    model = Session
    form_class = SessionUpdateForm

    # def form_valid(self, form):
    #     session = form.save(commit=False)
    #     session.owner = self.request.user
    #     session.save()
    #     self.object = session

    #     return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('session', kwargs={'session_id': self.object.id})


# API
class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


# API
class FobbitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fobbit.objects.all()
    serializer_class = FobbitSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ActiveQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = FobbitSerializer

    def get_queryset(self):
        return Fobbit.objects.filter(
            session__in=Session.objects.values_list('active_fobbit', flat=True))

    def retrieve(self, request, pk=None):
        fobbit = get_object_or_404(Session, id=pk).active_fobbit
        Session.objects.get(id=pk).active_fobbit
        serializer = FobbitSerializer(fobbit, context={'request': request})
        return Response(serializer.data)


class BluffViewSet(viewsets.ModelViewSet):
    serializer_class = BluffSerializer

    def get_queryset(self):
        if self.request.user:
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
