from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


#Product Categories
class Ecommerce_Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=15, blank=True)
    address1 = models.CharField(max_length=150, blank=True)
    address2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

def Create_Profile(sender, instance,created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(Create_Profile, sender=User)

class Ecommerce_Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Ecommerce_Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Ecommerce_Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    # ADD SALE PRICE
    is_sale = models.BooleanField(default=False)
    sale_price =  models.DecimalField(default=0, decimal_places=2, max_digits=6)
    def __str__(self):
        return f'{self.name} {self.price}'

# Customer Orders
class Ecommerce_Order(models.Model):
    product = models.ForeignKey(Ecommerce_Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Ecommerce_Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='',blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}'

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255, null=True, blank=True)
    shipping_province = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode =  models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
