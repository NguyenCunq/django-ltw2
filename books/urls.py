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
   path('', views.index, name='index'),
   path('book/<str:pk_test>/', views.book, name='book'),
   path('add_book/', views.addbook, name='add_book'),
   path('update_book/<str:pk>/', views.updatebook, name='update_book'),
   path('delete_book/<str:pk>/', views.deletebook, name='delete_book'),
   # path('update_book/<str:pk>/', views.updatebook, name="update_book"),
]