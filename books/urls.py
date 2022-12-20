from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
   path('admin/', admin.site.urls),
   path('login/', views.loginPage, name='login'),
   path('logout/', views.logoutUser, name="logout"),
   path('signup/', views.signupPage, name='signup'),
   path('adminmanager/',views.index, name='index'),
   path('book/<str:pk_test>/', views.book, name='book'),
   path('review/', views.Review_rate, name='review'),
   path('add_book/', views.addbook, name='add_book'),
   path('update_book/<str:pk>/', views.updatebook, name='update_book'),
   path('delete_book/<str:pk>/', views.deletebook, name='delete_book'),
   path('', views.storeUser, name='user'),
   path('category/<str:cat>/', views.CategoryView, name='category'),
   path('cart/', views.cart, name='cart'),
   path('checkout/', views.checkout, name='checkout'),
   path('update_item/', views.update_item, name='update_item'),
   path('process_order/', views.processOrder, name="process_order"),
   path('myaccount/', views.myaccount, name='myaccount'),
   # path('update_book/<str:pk>/', views.updatebook, name="update_book"),
]