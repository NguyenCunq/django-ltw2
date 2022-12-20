from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Book

CATEGORY = (
   ('fantasy','fantasy'),
   ('journal','journal'),
   ('honor','honor'),
   ('light novel','light novel')
)

class BookForm(forms.ModelForm):
   title = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
   author = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
   description = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
   page = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
   category = forms.ChoiceField(choices=CATEGORY)
   image = forms.ImageField()
   
   class Meta:
      model = Book
      fields = '__all__'

   def __init__(self, *args, **kwargs):
      super(BookForm, self).__init__(*args, **kwargs)
      self.fields['description'].required = False
      self.fields['image'].required = False

class UpdateBookForm(forms.ModelForm):

   title = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
   author = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
   description = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
   page = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
   category = forms.ChoiceField(choices=CATEGORY)
   image = forms.ImageField()

   class Meta:
      model = Book
      fields = '__all__'
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['description'].required = False

class CreateUserForm(UserCreationForm):
   class Meta:
      model = User
      fields = ['username', 'email', 'password1', 'password2']
