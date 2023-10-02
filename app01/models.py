
# Create your models here.
from django.db import models
# 建立資料庫
class EnglishWord(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField()

    def __str__(self):
        return self.word
#單選
class Academic(models.Model):
    topic = models.TextField()
    optionA = models.TextField()
    optionB = models.TextField()
    optionC = models.TextField()
    optionD = models.TextField()
    answer = models.CharField(max_length=10)
    year = models.CharField(max_length=10)
    topic_number = models.CharField(max_length=10)

    def __str__(self):
        return f"Topic: {self.topic}, Answer: {self.answer}, Year: {self.year}, Topic Number: {self.topic_number}"
      