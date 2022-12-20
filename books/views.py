from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

from .models import *
from .forms import BookForm, UpdateBookForm, CreateUserForm
from .role import unauthenticated_user, allowed_users
# Create your views here.
@unauthenticated_user
def loginPage(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None and user.is_superuser:
         login(request, user)
         return redirect('index')
      elif user is not None:
         login(request, user)
         return redirect('user')
      else:
         messages.info(request, 'username or password is incorrect')

   context = {}
   return render(request, 'login.html', context)


@unauthenticated_user
def signupPage(request):
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
@allowed_users(allowed_role=['admin'])
def index(request):
   books = Book.objects.all()
   context = {'books': books}
   return render(request, 'admin/home.html', context)


def book(request,pk_test):
   customer = request.user.customer
   book = Book.objects.get(id=pk_test)
   data = cartData(request)

   cartItems = data['cartItems']
   order = data['order']
   items = data['items']
   review = reversed(Review.objects.filter(book=book))
   count= Review.objects.filter(book=book).count()
   tb = 0
   for i in review:
      tb+=i.rate
   if count == 0:
      tb=0
   else:
      tb = round(tb/count,2)
   review = reversed(Review.objects.filter(book=book))
   context = {'book':book, 'customer':customer, 'review':review, 'cartItems': cartItems,'count':count, 'tb': tb}
   return render(request, 'store/book_detail.html', context)


def Review_rate(request):
   if request.method == 'GET':
      book_id = request.GET.get('book_id')
      book = Book.objects.get(id=book_id)
      comment = request.GET.get('comment')
      rate = request.GET.get('star')
      customer = request.user.customer
      Review(customer=customer, book=book, comment=comment, rate=rate).save()
      return redirect('book',book_id)

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def addbook(request):
   form = BookForm()
   if request.method == 'POST':
      form = BookForm(request.POST, request.FILES)
      if form.is_valid():
         form.save()
         return redirect('/')

   context = {'form': form}
   return render(request, 'admin/add_book.html', context)


@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def updatebook(request,pk):
   book= Book.objects.get(id=pk)
   form = UpdateBookForm(instance=book)
   if request.method == 'POST':
      form = UpdateBookForm(request.POST, request.FILES, instance=book) 
      if form.is_valid():
         form.save()
         return redirect('/book/'+pk)
   
   context = {'form': form, 'book': book}
   return render(request, 'admin/update_book.html', context)


@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def deletebook(request,pk):
   book = Book.objects.get(id=pk)
   if request.method == 'POST':
      book.delete()
      return redirect('/')

   context = {'item': book}
   return render(request, 'admin/delete.html', context)


def storeUser(request):
   customer = request.user.customer
   data = cartData(request)

   cartItems = data['cartItems']
   order = data['order']
   items = data['items']

   books = Book.objects.all()
   context = {'books': books, 'cartItems': cartItems, 'customer':customer}
   return render(request, 'store/userview.html', context)


def CategoryView(request,cat):
   customer = request.user.customer
   data = cartData(request)

   cartItems = data['cartItems']
   order = data['order']
   items = data['items']

   books = Book.objects.filter(category=cat)
   category = Category.objects.all()
   context = {'books': books, 'cartItems': cartItems, 'customer':customer, 'cat':category}
   return render(request, 'store/category.html',context)


def cart(request):
   customer = request.user.customer
   data = cartData(request)

   cartItems = data['cartItems']
   order = data['order']
   items = data['items']

   context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer':customer}
   return render(request, 'store/cart.html', context)


def checkout(request):
   customer = request.user.customer
   data = cartData(request)

   cartItems = data['cartItems']
   order = data['order']
   items = data['items']

   context = {'items': items, 'order': order, 'cartItems': cartItems, 'customer':customer}
   return render(request, 'store/checkout.html', context)


def update_item(request):
   data = json.loads(request.body)
   bookId = data['bookId']
   action = data['action']

   print('Action:',action)
   print('BookId:',bookId)

   customer = request.user.customer
   book = Book.objects.get(id=bookId)
   order, created = Order.objects.get_or_create(customer=customer,complete=False)
   
   orderItem, created = OrderItem.objects.get_or_create(order=order,book=book)
   
   if action == 'add':
      orderItem.quantity = (orderItem.quantity + 1)
   elif action == 'remove':
      orderItem.quantity = (orderItem.quantity - 1)

   orderItem.save()

   if orderItem.quantity <=0:
      orderItem.delete()
   return JsonResponse('Item was added', safe=False)


def processOrder(request):
   transaction_id = datetime.datetime.now().timestamp()
   data = json.loads(request.body)
   if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer,complete=False)

   else:
      customer, order = guestOrder(request, data)

   total = float(data['form']['total'])
   order.transaction_id = transaction_id

   if total == order.get_cart_total:
      order.complete = True
   order.save()

   if order.shipping == True:
      ShippingAddress.objects.create(
         customer=customer,
         order=order,
         address=data['shipping']['address'],
         city=data['shipping']['city'],
         district=data['shipping']['district'],
         zipcode=data['shipping']['zipcode'],
      )
   return JsonResponse('Payment submitted..', safe=False)


def myaccount(request):
   customer = request.user.customer
   data = cartData(request)
   cartItems = data['cartItems']
   order = Order.objects.filter(customer=customer,complete=True)
   print(order)
   orderItem = []
   for i in order:
      orderItem.append(OrderItem.objects.filter(order=i))
   orderItem.reverse()
   print(orderItem)
   context = {'order': order , 'orderItem': orderItem, 'customer':customer, 'cartItems': cartItems}
   return render(request,'store/myaccount.html', context)