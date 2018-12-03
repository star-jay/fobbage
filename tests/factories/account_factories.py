import factory

from fobbage.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'Jhon'
    last_name = 'Doe'
    email = factory.Sequence(lambda n: 'user{}@email.com'.format(n))
