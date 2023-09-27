
# Create your models here.
from django.db import models
# 建立資料庫
class EnglishWord(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField()

    def __str__(self):
        return self.word
#單選
class QuizQuestion(models.Model):
    TEXT_number = models.CharField(max_length=10,)
    topic = models.TextField()
    answer_options = models.CharField(max_length=100)
    answer = models.CharField(max_length=5)
    year = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.question_id}: {self.question_text}"
      