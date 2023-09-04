import json
from .models import *


def cookiecart(request):
    try:
      cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print('cart:',cart)
    items = []
    order = {'get_cart_total':0,'get_cart_item':0, 'shipping':False}
    cartitem = order['get_cart_item']
        
    for i in cart:
        try:
            cartitem += cart[i]['quantity']
                
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
                
            order['get_cart_total'] += total
            order['get_cart_item'] += cart[i]['quantity']
                
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)
                
            if product.digital == False:
                order['shipping'] = True
                
        except:
            pass
    return {'cartitem':cartitem, 'order':order, 'items':items}

def cartdata(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartitem = order.get_cart_item
    else:
       cookiedata = cookiecart(request)
       cartitem = cookiedata['cartitem']
       order = cookiedata['order']
       items = cookiedata['items']
    return {'cartitem':cartitem, 'order':order, 'items':items}

def guestorder(request, data):
    print('user is not logged in..')
        
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
        
    cookiedata = cookiecart(request)
    items = cookiedata['items']
        
    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()
        
    order = Order.objects.create(
        customer = customer,
        complete = False
    )
        
    for item in items:
        product = Product.objects.get(id = item['product']['id'])
            
        orderitem = OrderItem.objects.create(
            product=product,
            order = order,
            quantity = item['quantity']
        )
    return customer, order