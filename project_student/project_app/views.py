from django.contrib import messages
from django.http import request
from django.shortcuts import render, redirect
import requests
from . forms import *
from django.views import generic
from youtube_search import YoutubeSearch
from googleapiclient.discovery import build
import os
from .forms import DashboardForm
import wikipedia
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .forms import SignUpForm, LogInForm
from youtubesearchpython import VideosSearch
from .forms import CalculatorForm
# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"notes Added from{request.user.username} succesfully")
    else:
        form = NotesForm()
        notes = Notes.objects.filter(user=request.user)
        context = {"notes":notes,"form":form}
    return render(request, 'dashboard/notes.html', context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailview(generic.DetailView):
    model = Notes


def homework(request):

    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f'Homework added from{request.user.username}!!')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks':homework,
        'homeworks_done':homework_done,
        "form":form,
    }
    return render(request, 'dashboard/homework.html', context)


def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished == False
    else:
        homework.is_finished = True
        homework.save()
        return redirect("homework")


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


                            # YOUTUBE 
                            
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnails' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']

            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results': result_list
            }

        return render(request, 'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)
          
          
                                   # TO------DO -----
                                   
                                   
def todo(request):
    if request.method == 'POST':
        form  = TodoForm(request.POST)
        if form .is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
                todos = Todo(
                    user = request.user,
                    title = request.POST['title'],
                    is_finished = finished
                )
                todos.save()
                messages.success(request,f"Todo added from {request.user.username}")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        "todo": todo,
        'form': form,
        "todos_done":todos_done
    }

    return render(request, 'dashboard/todo.html', context)


def update_todo(request,pk=None):
    todos = Todo.objects.get(id=pk)
    if todos.is_finished == True:
        todos.is_finished = False
    else:
        todos.is_finished = True
    todos.save()
    return redirect("todo")

def delete_todo(request,pk=None):                               
    Todo.objects.get(id=pk).delete()
    return redirect('todo')
    

def Books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+text 
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                'subtitle' : answer['items'][i]['volumeInfo'].get('subtitle'),
                'description' : answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories' : answer['items'][i]['volumeInfo'].get('categories'),
                'rating' : answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail' : answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
                # preview is the link section when we click on any books inthe out it will redirect to the google 
                'link': answer['items'][i]['volumeInfo'].get('infoLink'),
            }            
            result_list.append(result_dict)
            context = {
                'form':form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html',context)
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/books.html', context)


def Dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+ text 
            r = requests.get(url)
            if r.status_code == 200:
                try:
                    answer = r.json()
                    phonetics = answer[0]['phonetics'][0]['text']
                    audio = answer[0]['phonetics'][0]['audio']
                    definition = answer[0]['meanings'][0]['definitions'][0]['definition']
                    example = answer[0]['meanings'][0]['definitions'][0]['example']
                    synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
                    context = {
                        'form': form,
                        'input': text,
                        'phonetics': phonetics,
                        'audio': audio,
                        'definition': definition,
                        'example': example,
                        'synonyms': synonyms
                    }
                except (IndexError, KeyError):
                    context = {
                        'form': form,
                        'input': text,
                        'error_message': 'No definition found for the given word.'
                    }
            else:
                context = {
                    'form': form,
                    'input': '',
                    'error_message': 'Failed to fetch data from the API.'
                }
        else:
            context = {'form': form}
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary,        
        }
        return render(request, "dashboard/wiki.html", context)
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, "dashboard/wiki.html", context)

                        

# views.py

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user = form.save(commit=False)
                user.password = make_password(password)
                user.save()
                return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'dashboard/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()
            messages.success(request, f"Account created for {user} successfully " )
            if user and check_password(password, user.password):
                # Redirect to home page
                return redirect('home')
            else:
                # Show input validation error
                return render(request, 'dashboard/login.html', {'form': form, 'error': True})
    else:
        form = LogInForm()
    return render(request, 'dashboard/login.html', {'form': form, 'error': False})

def profile(request):
    homeworks = Homework.objects.filter(is_finished = False,user=request.user)
    todo = Todo.objects.filter(is_finished = False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True 
    else:
        homework_done = False    
        
    if len(todo) == 0:
        todo_done = True 
    else:
        todo_done = False    
    context = {
        'homeworks':homeworks,
        'todo': todo,
        'homework_done':homework_done,
        'todo_done': todo_done,
    }     
    return render(request, 'dashboard/profile.html', context)

          # CALCULATOR
          
          
def calculator(request):
    result = None
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            number1 = form.cleaned_data['number1']
            number2 = form.cleaned_data['number2']
            operation = form.cleaned_data['operation']
            if operation == 'add':
                result = number1 + number2
            elif operation == 'subtract':
                result = number1 - number2
            elif operation == 'multiply':
                result = number1 * number2
            elif operation == 'divide':
                if number2 != 0:
                    result = number1 / number2
                else:
                    result = 'Cannot divide by zero'
    else:
        form = CalculatorForm()
    return render(request, 'dashboard/calculator.html', {'form': form, 'result': result})          