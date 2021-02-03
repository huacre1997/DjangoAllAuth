from decimal import Decimal 
from django.conf import settings 
from django.apps import apps
from json import JSONEncoder
import json
class Cart(object):
    model = apps.get_model('products', 'Product')

    def __init__(self, request):
        self.session = request.session        
        cart = self.session.get(settings.CART_SESSION_ID)  
        if not cart:         
            cart = self.session[settings.CART_SESSION_ID] = {}        
        self.cart = cart
    def exists(self, id):
        return True if str(id) in list(self.cart.keys()) else False
           
        
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)   
          
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,'price': str(product.price),"image":str(product.image),"name":str(product.name),"marca":str(product.marca)}        
        if override_quantity:  
          
            self.cart[product_id]['quantity'] = quantity        
        else:   
         
            self.cart[product_id]['quantity'] += quantity        
        self.save()
    def save(self):       
        self.session.modified = True 
    def remove(self, product):  
        product_id = str(product.id)        
        if product_id in self.cart:            
            # del self.cart[product_id]            
            self.save() 

    def update(self, product,quantity):  
        product_id = str(product.id)        
        if product_id in self.cart: 
            if quantity==0:
                del self.cart[product_id]            

            else:  
                self.cart[product_id]['quantity'] = quantity 
            
            self.save() 
    def __iter__(self):     
        product_ids = self.cart.keys()      
        products = self.model.objects.filter(id__in=product_ids)
        cart = self.cart.copy()        
        for product in products:            
            cart[product.id]['product'] = product
        for item in cart.values():            
            item['price'] = Decimal(item['price'])            
            item['total_price'] = item['price'] * item['quantity']            
            yield item
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values()) 
    def get_total_price(self):        
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) 
    def clear(self):      
        del self.session[settings.CART_SESSION_ID]
        self.save() 

