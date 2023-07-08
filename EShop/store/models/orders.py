from django.db import models
from .product import Product
from .customer import Customer
import datetime


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    customer =models.ForeignKey(Customer, on_delete=models.CASCADE) 
    quantity =models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=100,default='' , blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False )

    @staticmethod
    def placeOrder(self):
        return self.save()
    
    @staticmethod
    def get_orders_by_customerId(customerId):
        return Order.objects.filter(customer = customerId).order_by('date')
 