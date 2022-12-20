from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
   name = models.CharField(max_length=100)

   def __str__(self):
      return self.name

class Book(models.Model):
   CATEGORY = (
      ('Phiêu lưu','Phiêu lưu'),
      ('Kinh dị','Kinh dị'),
      ('Trinh thám','Trinh thám'),
      ('light novel','light novel'),
      ('E-book','E-book'),
      ('Văn học Việt Nam','Văn học Việt Nam'),
      ('Văn học Nước Ngoài','Văn học Nước Ngoài'),

   )
   title = models.CharField(max_length=200, null=True, db_index=False)
   author = models.CharField(max_length=200, null=True)
   category = models.CharField(max_length=200, null=True, choices=CATEGORY)
   date = models.DateField(auto_now_add=True, null=True)
   page = models.IntegerField(null=True)
   description = models.CharField(max_length=20000, blank=True)
   image = models.ImageField(upload_to='image',null=True, default="image/123.jpg")
   price = models.FloatField(null=True)
   digital = models.BooleanField(default=False,blank=True)

   def __str__(self):
      return self.title


class Customer(models.Model):
   user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
   name = models.CharField(max_length=200,null=True)
   email = models.CharField(max_length=200, null=True)
   profile_pic = models.ImageField(upload_to='image',null=True, blank=True, default="image/useravt.png")

   def __str__(self):
      return self.name


class Review(models.Model):
   customer = models.ForeignKey(Customer,models.CASCADE)
   book = models.ForeignKey(Book, models.CASCADE)
   comment = models.TextField(max_length=1000)
   rate = models.IntegerField(default=0)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return str(self.id)


class Order(models.Model):
   customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
   date = models.DateField(auto_now_add=True)
   complete = models.BooleanField(default=False)
   transaction_id = models.CharField(max_length=200,null=True)

   def __str__(self):
      return str(self.id)

   def get_date(self):
      return self.date

   def get_shipinfo(self):
      return self.shipping.address

   @property
   def shipping(self):
      shipping = False
      orderitems = self.orderitem_set.all()
      for i in orderitems:
         if i.book.digital == False:
            shipping = True
         return shipping

   @property
   def get_cart_total(self):
      orderitems = self.orderitem_set.all()
      total = sum ([item.get_total for item in orderitems])
      return total

   @property
   def get_cart_items(self):
      orderitems = self.orderitem_set.all()
      total = sum([item.quantity for item in orderitems])
      return total

class OrderItem(models.Model):
   book = models.ForeignKey(Book,on_delete=models.SET_NULL,null=True,blank=True)
   order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
   quantity = models.IntegerField(default=0,null=True,blank=True)
   date_added = models.DateTimeField(auto_now_add=True)

   @property
   def get_total(self):
      total = self.book.price * self.quantity
      return total
   def get_date(self):
      return self.order.date
   def get_order(self):
      return self.order.shipping

class ShippingAddress(models.Model):
   customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
   order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
   address = models.CharField(max_length=200, null=True)
   city = models.CharField(max_length=200, null=True)
   district = models.CharField(max_length=200, null=True)
   zipcode = models.CharField(max_length=200, null=True)
   date_added = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.address