import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
# model for storing user info
class User(AbstractUser):
    pass
# model for storing question info
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    MY_CHOICES = (('Anime', 'Anime'),('Football', 'Football'),('Framework', 'Framework'),('Other', 'Other'),)
    my_field = models.CharField(max_length=20, choices=MY_CHOICES, null=True)
    pub_date = models.DateTimeField('date published')
    username = models.CharField(max_length=20)

    def __str__(self):
        return self.question_text
# model for storing choice info
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
# model for storing editing choice info
class Change_choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    new_choice = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
# model to ensure user only vote once
class Vote_count(models.Model):
    question_voted = models.IntegerField(default=0)
    voter = models.IntegerField(default=0)