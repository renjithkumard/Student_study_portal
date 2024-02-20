from django import forms
from django.forms import DateInput
from . models import *
# myapp/forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Todo 
from django.contrib.auth.models import User
from .models import User
        
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
         }
         
        fields = ['title', 'description']
class DateInput(forms.DateInput):
    input_type = 'date'

class MyCheckboxForm(forms.Form):
    is_checked = forms.BooleanField(
    )
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {
        'subject': forms.TextInput(attrs={'class': 'form-control'}),
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'is_finished': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        'due': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        fields = ['subject', 'title', 'description', 'due','is_finished']

# class YouTubeSearchForm(forms.Form):
#     text = forms.CharField( max_length=100,label='Search Youtube:')

class DashboardForm(forms.Form):
    text = forms.CharField(
        label='Search', 
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Search', 'class': 'search-box'})
        ) 
    class Media:
        css = {
            'all': ('CSS/search.css',)  # Replace 'search_form.css' with your actual CSS file name
        }
    #forms.CharField(max_length=100,label='Enter your Search:')

class YouTubeSearchForm(forms.Form):
    query = forms.CharField(label='Search YouTube')

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo 
        fields = ['title', 'is_finished']
               
               

# forms.py

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CalculatorForm(forms.Form):
    number1 = forms.FloatField(label='Number 1')
    number2 = forms.FloatField(label='Number 2')
    operation = forms.ChoiceField(label='Operation', choices=[
        ('add', 'Addition'),
        ('subtract', 'Subtraction'),
        ('multiply', 'Multiplication'),
        ('divide', 'Division'),
    ])
