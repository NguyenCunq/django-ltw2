from django.db import models

class Book(models.Model):
   CATEGORY = (
      ('fantasy','fantasy'),
      ('journal','journal'),
      ('honor','honor'),
      ('light novel','light novel')
   )
   title = models.CharField(max_length=200, null=True)
   author = models.CharField(max_length=200, null=True)
   category = models.CharField(max_length=200, null=True, choices=CATEGORY)
   date = models.DateField(auto_now_add=True, null=True)
   page = models.IntegerField(null=True)
   description = models.CharField(max_length=200, blank=True)
   image = models.ImageField(upload_to='image',null=True, default="image/123.jpg")

   def __str__(self):
      return self.title