from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import *

# Create your views here.

def login(request):
    data = cartdata(request)
    cartitem = data['cartitem']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartitem':cartitem}
    return render(request, "store/login.html", context)

def store(request):
    
    data = cartdata(request)
    cartitem = data['cartitem']
        
    product = Product.objects.all()
    context = {'products':product, 'cartitem':cartitem}
    return render(request, "store/store.html", context)

def cart(request):
    data = cartdata(request)
    cartitem = data['cartitem']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartitem':cartitem}
    return render(request, "store/cart.html", context)

def checkout(request):
    
    data = cartdata(request)
    cartitem = data['cartitem']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartitem':cartitem}
    return render(request, "store/checkout.html", context)

def updateitem(request):
    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']
    
    print('action:',action)
    print('productis:',productid)
    
    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(customer=customer, complete = False)
    
    orderitem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
        
    orderitem.save()
    
    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse("item was added", safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        
    else:
        customer, order = guestorder(request, data)
            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    if total == order.get_cart_total:
        order.complete = True
    order.save()
        
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
            country = data['shipping']['country']
        )
        
    return JsonResponse("payment complete", safe=False)