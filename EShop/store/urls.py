
from django.contrib import admin
from django.urls import path
from .views  import index
from .views  import signup
from .views  import login
from .views import logout
from .views import cart
from .views import checkout
from .views import orders
from .middlewares.auth import auth_middleware

urlpatterns = [
    path('',index.as_view() , name="home"),
    path('signup', signup.as_view() , name="signup"),
    path('login', login.as_view() , name="login"),
    path('logout', logout , name="logout"),
    path('cart', cart.as_view() , name="cart"),
    path('checkout', checkout.as_view() , name="checkout"),
    path('orders', auth_middleware(orders.as_view()) , name="orders"),
    # path('orders', orders.as_view() , name="orders"),
]
