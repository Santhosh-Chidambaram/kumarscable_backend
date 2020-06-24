from django.shortcuts import render
from Customers.models import Customer,CustomerReport
from django.contrib.auth.mixins import LoginRequiredMixin
from Collections.models import CollectedCustomer,Collection
from django.utils.decorators import method_decorator
import datetime
from django.views.generic import View
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,reverse,get_object_or_404
# Create your views here.

#Main Dashboard
def HomeView(request):
    return render(request,'Dashboard/login.html')

#Login View

class LoginView(View):
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            return redirect('kc_admin_dashboard')
        return HttpResponseRedirect(reverse("user_login"))
    
    def get(self,request):
        return render(request,'Dashboard/login.html')

def user_logout(request):
    logout(request)
    return redirect('kc_home')




class DashboardView(LoginRequiredMixin,View):
    def get(self,request):
        customer = Customer.objects.all()
        total_share = collected_amount = due_amount = 0
        paidcus = customer.filter(payment_status='paid')
        unpaidcus = customer.filter(payment_status='unpaid')
        paid = customer.filter(payment_status='paid').count()
        unpaid = customer.filter(payment_status='unpaid').count()
        for c in customer:
            total_share+=c.payment_amount
        for c in paidcus:
            collected_amount+=c.payment_amount
        for c in unpaidcus:
            due_amount+=c.payment_amount
        context ={
            "customer":customer,
            "paidcount":paid,
            "unpaidcount":unpaid,
            "total_share":total_share,
            "due_amount":due_amount,
            "collected_amount":collected_amount
        }
        return render(request,'Dashboard/dashboard.html',context) 

#Customers 

def CustomerStatusView(request):
    status = request.GET.get('status')
    cus = Customer.objects.all()
    cusobj = cus.filter(payment_status=status)
    context = {
            "status":status,
            "customers":cusobj,
            "count":cusobj.count()
        }
    return render(request,'Dashboard/customers.html',context)



#Daily Collected

def Collected_Customers(request):
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    try:
        coll = CollectedCustomer.objects.filter(collected_date__contains=date)
    except TypeError:
        pass
    total_collection = 0
    for c in coll:
        total_collection+=c.collected_amount
       

    context = {
        "total_collection":total_collection,
        "collected_customers":coll,
        "total_count":coll.count()
    }
    return render(request,'Dashboard/collected_customers.html',context)


#Collection Reports
def CollectionView(request):
    coll = Collection.objects.all()
    overall_collection = 0
    for o in coll:
        overall_collection+=o.collection_amount
    context = {
        "collection":coll,
        "overall_collection":overall_collection
    }
    return render(request,'Dashboard/collection.html',context)

#Collection Customers List
def CollectionListView(request,pk):
    coll = get_object_or_404(Collection,id=pk)
    context = {
        "coll":coll,
    
        
    }
    return render(request,'Dashboard/collectionlist.html',context)

#Monthly Payment Reports
def CustomerPaymentReports(request):
    cpr = CustomerReport.objects.all()
    cprcount = cpr.count() 
    context = {
        'cpr':cpr,
        'cprcount':cprcount
    }
    return render(request,'Dashboard/customer_report.html',context)


#Report Problem to Customers

# def CustomerSupportView(request):
#     street = Customer.objects.order_by().values('street').distinct()
#     context ={
#         "street":street
#     }
#     return render(request,'Dashboard/customer_support.html',context)