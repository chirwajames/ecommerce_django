from django.contrib.auth import admin
from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index, name="home"),
    path('home/', views.index, name="index"),
    path('login/',views.login_user, name="login"),
    path('logout/', views.logout_user,name="logout"),
    path('register/', views.register_user,name="register"),
    path('cart_summary/', views.cart_summary, name="cart_summary"),
    path('product/<int:pk>', views.view_item, name="product"),
    path('add_cart/', views.add_cart_item, name="add_cart_item"),
    path('delete_cart_item/', views.delete_cart_item, name="delete_cart_item"),
    path('update_user/', views.update_user, name="update_user"),
    path('payment-success/', views.payment_success, name="payment_success"),
    path('payment/', views.payment, name="payment"),
    path('profile/',views.profile, name="user_profile"),#update_info
    path('search/',views.search, name="search"),
    path('category_summary/',views.category_summary, name="category_summary"),
    path('category/<str:foo>',views.categories, name="category"),
    path('update_password/',views.update_password, name="update_password")

]