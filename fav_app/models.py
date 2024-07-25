from django.db import models
import bcrypt
import re
from datetime import datetime 
from django.core.exceptions import ObjectDoesNotExist

class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['firstname']) < 2:
            errors["firstname"] = "First name should be at least 2 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if  User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists"
        if postData['password'] != postData['copassword']:
            errors['password_match'] = "Passwords do not match"
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"
        return errors
    # add validations to the log in
    def basic_validatorlogin(self,postData):
            errors = {}
            try:
                user = User.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors['email'] = "Email not found."
                return errors
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password."
            return errors
    # add validation to the title and description
    def book_validator(self, postData):
        errors = {}
        if 'title' not in postData or len(postData['title']) == 0:
            errors["title"] = "Title is required"
        if len(postData['desc']) < 5:
            errors["desc"] = "Description should be at least 5 characters"
        return errors


class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    copassword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # liked_books = a list of books a given user likes
    # books_uploaded = a list of books uploaded by a given user
    def __str__(self):
        return f"{self.firstname}"
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # uploaded_by = user who uploaded a given book
    # users_who_like = a list of users who like a given book
    def __str__(self):
        return f"{self.title}"
    
def all_books():
    return Book.objects.all()

def all_users():
    return User.objects.all()

def get_book_id(book_id):
    return Book.objects.get(id=book_id)

def get_user_id(user_id):
    return User.objects.get(id=user_id)

def add_regestraion(POST):
    password = bcrypt.hashpw(POST['password'].encode(), bcrypt.gensalt()).decode()
    copassword=bcrypt.hashpw(POST['copassword'].encode(), bcrypt.gensalt()).decode()
    registration = User.objects.create(
        firstname=POST['firstname'],
        lastname=POST['lastname'],
        email=POST['email'],
        password=password,
        copassword=copassword
    )
    return registration

def add_books(request, POST):
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title=POST['title'],
            desc=POST['desc'],
            uploaded_by=user
        )
        return book

def update_books(POST,book_id):
    book = Book.objects.get(id=book_id)
    book.title =POST['title']
    book.desc = POST['desc']
    book.save()

def delete_books(book_id):
        book = Book.objects.get(id=book_id)
        book.delete()

