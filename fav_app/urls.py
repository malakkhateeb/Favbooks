from django.urls import path     
from . import views

urlpatterns = [
    path('', views.logIn),
    path('register', views.addRegistrations),
    path('login', views.addLogin),
    path('books', views.books),
    path('books/add', views.addBooks),
    path('books/<int:book_id>/favorite', views.favoriteBook),
    path('books/<int:book_id>/unfavorite', views.unfavoriteBook),
    path('books/<int:book_id>/update', views.updateBooks),
    path('books/delete', views.deleteBook),
    path('books/<int:book_id>', views.showBook),
    path('logout', views.logOut),
]