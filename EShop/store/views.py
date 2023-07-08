from django.shortcuts import redirect, render
from django.http import HttpResponse
# Create your views here.
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .models.orders import Order
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator

class index(View):
    def get(self, request):
        data = {}
        products = None 
        cart = request.session.get('cart')
        if not cart:
            request.session['cart']={}
            
        categories = Category.get_all_categories()
        categoryId = request.GET.get('category')
        if categoryId:
            products = Product.get_all_products_by_categoryId(categoryId)
        else:
            products = Product.get_all_products()
        data['products'] = products
        data['categories'] = categories
        return render(request, 'index.html', data)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        print(product)
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            print(quantity)
            if quantity :
                if remove :
                    if quantity :
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart']=cart
        print(request.session['cart'])
        return redirect('home')


class signup(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(Self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)

        error_message = None
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'

        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('login')

        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)


class login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = Customer.getCustomerByEmailId(email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                
                return redirect('home')
            else:
                error_message = 'Email or password invalid'

        else:
            error_message = 'Email or password invalid'
        return render(request, 'login.html', {'error': error_message})


class cart(View):
    def get(self,request):
        productIds = list(request.session.get('cart').keys())
        products = Product.get_all_products_by_productId(productIds)
        return render(request , 'cart.html' , {'products' : products})


class checkout(View):

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer_id')
        print(address, phone, customer)
        cart = request.session.get('cart')
        products = Product.get_all_products_by_productId(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        return redirect('cart')


class orders(View):
    # @method_decorator(auth_middleware)
    def get(self,request):
        customer = request.session.get('customer_id')
        orders = Order.get_orders_by_customerId(customer)
        print(orders)
        return render (request ,'orders.html', {'orders':orders})



def logout(request):
    request.session.clear()
    return redirect("login")