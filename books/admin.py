from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
   list_display = ['id','customer','book','rate','created_at']
   readonly_fields = ['created_at'] 