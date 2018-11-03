"""
The different models that together make out a quiz
"""

from django.db import models


class Quiz(models.Model):
    title = models.CharField(
        max_length=255,
    )

    def __str__(self):
        """ string representation """
        if self.title:
            return "Quiz: {}".format(self.title)
        else:
            return "Quiz: unnamed quiz"
