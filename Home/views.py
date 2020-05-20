from django.shortcuts import render,redirect,reverse
from .models import *
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib import messages
# Create your views here.
def homeView(request):
    carousel = CarouselSet.objects.all()
    return render(request,'home/index.html',{"carousel":carousel})

def ContactusView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        messages.success(request,f"Your query has been successfully submitted")
        cf = ContactForm(name=name,email=email,subject=subject,message=message)
        cf.save()
        return redirect('home')
        


class InvoiceView(View):
    def post(self,request):
        query = request.POST.get('boxno')
        q_box = Customer.objects.filter(setupbox__boxno=query)
        if q_box:
            context ={
            "pay": [
            
                {
                    "name":s.name,
                    "street":s.street,
                    "phone":s.phone,
                    "setupbox":
                        {
                        
                        "boxno":s.setupbox.boxno,
                        "cafnum":s.setupbox.cafnum,
                        "base_package":s.setupbox.base_package,
                        "bouquets":str([p.name for p in s.setupbox.bouquets.all()])[1:-1],
                        "bcbouquets":str([p.name for p in s.setupbox.broadcast_bouquets.all()])[1:-1],
                        "addon_packages":str([p.name for p in s.setupbox.addon_packages.all()])[1:-1],
                        "start_date":s.setupbox.start_date,
                        "end_date":s.setupbox.end_date,
                        "price":s.setupbox.price,
                        "add_price":s.setupbox.additional_price,
                        "total_price":s.setupbox.price+s.setupbox.additional_price
                        },
                    "payment_amount":s.payment_amount

                    } for s in q_box
            ],
            "paymentView":True
            }
            return render(request,'home/invoice.html',context)
    
# @csrf_exempt  
# def checkout(request):
#     if request.method == 'POST':
#         name = request.POST.get('name','')
#         phone = request.POST.get('phone','')
#         amt = request.POST.get('amount','')
#         print(name,phone,amt)
#         pay = Payment(name=name,phone=phone,amount=amt )
#         pay.save()
#         return redirect('home')
    
