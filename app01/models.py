

# Create your models here.
from django.db import models

class EnglishWord(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField()

    def __str__(self):
        return self.word
