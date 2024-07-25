from django.shortcuts import render, redirect
from .models import*
from django.contrib import messages
# this method render the main page to add Registration or to log in 
def logIn(request):
    context={
        'users':all_users(),
    }
    return render(request, 'index.html', context)
# _______________________________________________________________________________
#this method to add new user to database
def addRegistrations(request):
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
    if request.method == 'POST':
            user=add_regestraion(request.POST)
            request.session['user_id'] = user.id 
            messages.success(request, "Successfully registered")
            
    return redirect('/')
# -------------------------------------------------------------------------
#this method to add the email and passswored and hash the password and returns the error when logi with email and password invalid
def addLogin(request):
    errors = User.objects.basic_validatorlogin(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
    
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/books')
        messages.error(request, 'Invalid login credentials')
        return redirect('/')
    return redirect('/')
# ___________________________________________________________________________________________________________________
# Displays the books page if the user is logged in,Passes the logged-in user and all books to the addfav.html template.
def books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': get_user_id(request.session['user_id']),
        'books': all_books()
    }
    
    return render(request, 'books_list.html', context)
# __________________________________________________________________________
# add new book with title and description on addfav.html 
def addBooks(request):
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            add_books(request, request.POST)
            return redirect('/books')
# ________________________________________________________________________________________
# Allows the logged-in user to mark a book as their favorite.
def favoriteBook(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user =  get_user_id(request.session['user_id'])
    book = get_book_id(book_id)
    book.users_who_like.add(user)
    return redirect(f'/books/{book_id}')
# _______________________________________________________________________________________
# Allows the logged-in user to remove a book from their favorites.
def unfavoriteBook(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = get_user_id(request.session['user_id'])
    book =  get_book_id(book_id)
    book.users_who_like.remove(user)
    return redirect(f'/books/{book_id}')
# ________________________________________________________________________________________
# to check if the logged-in user can update a book, compare the user_id stored in the session with the uploaded_by ID of the book:
def updateBooks(request, book_id):
    get_book = get_book_id(book_id)
    logged_in_user_id = request.session.get('user_id')
    context = {
        'book': get_book_id(book_id),
        'user': get_user_id(request.session['user_id'])
    }
    if request.method == 'POST' and logged_in_user_id == get_book.uploaded_by.id:
        errors = User.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/books/{book_id}')
        else:
            update_books(request.POST,book_id)
            return redirect(f'/books/{book_id}')
    
    return render(request, 'edit.html', context)
# _________________________________________________________________________________________________________________________
# Allows the logged-in user who uploaded the book to delete it.
def deleteBook(request):
    get_book = get_book_id(request.POST['id'])
    logged_in_user_id = request.session.get('user_id')
    if request.method == 'POST' and logged_in_user_id == get_book.uploaded_by.id:
        delete_books(request.POST['id'])
    return redirect('/books')
# ____________________________________________________________________________________________________________________
def showBook(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'book': get_book_id(book_id),
        'user': get_user_id(request.session['user_id'])
    }
    return render(request, 'show.html', context)
# _______________________________________________________________________________________________________________________
#this method clean the sessions when log out 
def logOut(request):
    request.session.clear()
    return redirect('/')
