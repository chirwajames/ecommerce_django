from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Ecommerce_Category)
admin.site.register(Ecommerce_Customer)
admin.site.register(Ecommerce_Product)
admin.site.register(Ecommerce_Order)
admin.site.register(ShippingAddress)
admin.site.register(Profile)


class ProfileInLine(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username','first_name','last_name','email']
    inlines = ProfileInLine

#admin.site.unregister(User)

#admin.site.register(User, UserAdmin)