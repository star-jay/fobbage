import environ
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from fobbage.quizes.models import Quiz, Round, Question

env = environ.Env()
User = get_user_model()


# USER_SPECS = [
#     {
#         'email': 'oda@university.eu',
#         'first_name': 'Oda',
#         'last_name': 'Muller',
#         'password': 'not so safe'
#     }
# ]

QUIZ = {
    'title': 'My first quiz',
    'rounds': [
        {
            'title': 'First round',
            'questions': [
                {
                    'text': 'How many lines of code did I write?',
                    'correct_answer': '5, it was not a good day',
                },
                {
                    'text': 'What is my bowling alias',
                    'correct_answer': 'David bowlie',
                },
                {
                    'text': 'Complete this sentance hakuna __',
                    'correct_answer': 'Matata',
                },
            ]
        },
        {
            'title': 'Second round',
            'questions': [
                {
                    'text': 'Name the most useless dungeon and dragons spell',
                    'correct_answer': 'create food and water',
                },
                {
                    'text': 'Name a dance move',
                    'correct_answer': 'jazz fingers',
                },
                {
                    'text': 'LSD stands for',
                    'correct_answer': 'lucy in the sky with diamonds',
                }
            ]
        }
    ]
}


class Command(BaseCommand):
    help = 'Loads initial data for Fobbage'

    def create_superuser_from_env(self):
        """creates a super user if info is in .env file"""
        if env.str('DEFAULT_ADMIN_EMAIL', None) and env.str(
           'DEFAULT_ADMIN_PASSWORD', None):
            self.stdout.write('Create superuser...')
            User.objects.create_superuser(
                email=env.str('DEFAULT_ADMIN_EMAIL'),
                password=env.str('DEFAULT_ADMIN_PASSWORD'),
            )
        else:
            self.stdout.write(
                'No superuser info found in the environment file...')

    def create_quiz(self):
        quiz = Quiz.objects.create(title=QUIZ['title'])
        for r in QUIZ['rounds']:
            round = Round.objects.create(
                quiz=quiz,
                title=r['title'],
            )
            for q in r['questions']:
                Question.objects.create(
                    round=round,
                    text=q['text'],
                    correct_answer=q['correct_answer'],
                )

    def handle(self, *args, **options):
        self.stdout.write('Creating superuser from env-file')
        self.create_superuser_from_env()

        self.stdout.write('Create first quiz')
        self.create_quiz()
