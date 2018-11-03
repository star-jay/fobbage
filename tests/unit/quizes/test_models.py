import pytest

from tests.factories.quiz_factories import (
    QuizFactory,
)


@pytest.mark.django_db
def test_quiz_string_representation():
    """Make a clear string representation for the quiz"""
    quiz = QuizFactory()

    assert quiz.__str__() == 'Quiz: ' + str(quiz.title)
