import environ
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


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

    def handle(self, *args, **options):
        self.stdout.write('Creating superuser from env-file')
        self.create_superuser_from_env()


