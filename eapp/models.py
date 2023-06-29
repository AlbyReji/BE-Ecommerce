from django.db import models
import datetime
from django.contrib.auth.models import User
import os

# Create your models here.
def getFileName(request,filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class Category(models.Model):
    name = models.CharField(max_length=150,null =False,blank = True)
    image = models.ImageField( upload_to=getFileName,null =False,blank = True)
    description = models.TextField(max_length=400,null =False,blank = True)
    status = models.BooleanField(default = False,help_text ="0-show,1-hidden")
    created_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    Category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null =False,blank = True)
    vendor = models.CharField(max_length=150,null =False,blank = True)
    Product_image = models.ImageField( upload_to=getFileName,null =False,blank = True)
    quantity = models.IntegerField(null =False,blank = True)
    price = models.IntegerField(null =False,blank = True)
    description = models.TextField(max_length=400,null =False,blank = True)
    status = models.BooleanField(default = False,help_text ="0-show,1-hidden")
    created_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)
  created_at=models.DateTimeField(auto_now_add=True)


  @property
  def total_cost(self):
    return self.product_qty * self.product.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)





