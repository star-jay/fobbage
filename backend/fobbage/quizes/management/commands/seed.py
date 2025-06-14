from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from fobbage.accounts.models import User
from fobbage.quizes.models import Quiz, Question, Session, Fobbit, Score, Answer, Bluff, Guess, LikeAnswer

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        models = [Quiz, Question, Session, Fobbit, Score, Answer, Bluff, Guess, LikeAnswer, User]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        # Create superuser using management command
        call_command('createsuperuser', '--no-input', interactive=False)
        superuser = User.objects.get(is_superuser=True)

        # Create regular users
        user1 = User.objects.create_user(username='player1', password='password123', first_name='Player', last_name='One')
        user2 = User.objects.create_user(username='player2', password='password123', first_name='Player', last_name='Two')
        user3 = User.objects.create_user(username='player3', password='password123', first_name='Player', last_name='Three')

        # Create a quiz
        quiz = Quiz.objects.create(
            title='General Knowledge Quiz',
            created_by=superuser
        )

        # Add questions to the quiz
        question1 = Question.objects.create(
            quiz=quiz,
            text='What is the capital of France?',
            correct_answer='Paris',
            order=1,
            player=superuser
        )

        question2 = Question.objects.create(
            quiz=quiz,
            text='What is 2 + 2?',
            correct_answer='4',
            order=2,
            player=superuser
        )
        
        question3 = Question.objects.create(
            quiz=quiz,
            text='Who wrote "To Kill a Mockingbird"?',
            correct_answer='Harper Lee',
            order=3,
            player=superuser
        )

        # Create a quiz session
        session = Session.objects.create(
            quiz=quiz,
            name='Weekly Quiz Night',
            owner=superuser,
        )

        # Add players to the session
        session.players.add(user1, user2, user3)
        session.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.')) 