from django.urls import path, include
from .import views
urlpatterns = [
    path('', views.home, name="home"),

    # Notes section
    path('notes/', views.notes, name="notes"),
    path('delete_note/<int:pk>', views.delete_note, name="delete_note"),
    path('notes_detail/<int:pk>', views.NotesDetailview.as_view(), name="notes-detail"),

    # Homework section
    path('homework/', views.homework, name="homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update_homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete_homework"),

    #Youtube section
    path('youtube', views.youtube, name="youtube"),

    #TO-DO
    path('todo', views.todo, name="todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update_todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete_todo"),
    
    # BOOKS
    path('books', views.Books, name="books"),
    
    path('dictionary', views.Dictionary, name="dictionary"),
    path('wiki', views.wiki, name='wiki'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('Profile/', views.profile, name='profile'), 
    
    path('calculator/', views.calculator, name='calculator'),
]




