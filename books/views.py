from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import BookForm, UpdateBookForm, CreateUserForm

# Create your views here.
def loginPage(request):
   if request.user.is_authenticated:
      return redirect('index')
   else:
      if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(request, username=username, password=password)
         if user is not None:
            login(request, user)
            return redirect('index')
         else:
            messages.info(request, 'username or password is incorrect')

      context = {}
      return render(request, 'login.html', context)

def signupPage(request):
   if request.user.is_authenticated:
      return redirect('index')
   else:
      form = CreateUserForm()
      if request.method == 'POST':
         form = CreateUserForm(request.POST)
         if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'User created successfully for '+user)
            return redirect('login')

      context = {'form': form}
      return render(request, 'signup.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def index(request):
   books = Book.objects.all()
   context = {'books': books}
   return render(request, 'home.html', context)

@login_required(login_url='login')
def book(request,pk_test):
   book = Book.objects.get(id=pk_test)
   context = {'book':book}
   return render(request, 'book_detail.html', context)

@login_required(login_url='login')
def addbook(request):
   form = BookForm()
   if request.method == 'POST':
      form = BookForm(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('/')

   context = {'form': form}
   return render(request, 'add_book.html', context)

@login_required(login_url='login')
def updatebook(request,pk):
   book= Book.objects.get(id=pk)
   form = UpdateBookForm(instance=book)
   if request.method == 'POST':
      form = UpdateBookForm(request.POST, request.FILES, instance=book) 
      if form.is_valid():
         form.save()
         return redirect('/book/'+pk)
   
   context = {'form': form, 'book': book}
   return render(request, 'update_book.html', context)

@login_required(login_url='login')
def deletebook(request,pk):
   book = Book.objects.get(id=pk)
   if request.method == 'POST':
      book.delete()
      return redirect('/')

   context = {'item': book}
   return render(request, 'delete.html', context)