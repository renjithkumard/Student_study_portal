from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.forms import Field


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # when user deleted the notes it also get deleted in the data base
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description  = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    is_finished = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=50, default = 'Username')
    first_name = models.CharField(max_length=50, default = 'first name')
    last_name = models.CharField(max_length=50, default = 'last name')
    email = models.EmailField(unique=True, default = 'email')
    password = models.CharField(max_length=100, default = 'password')

    def __str__(self):
        return self.username