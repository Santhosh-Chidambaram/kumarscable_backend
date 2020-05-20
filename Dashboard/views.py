from django.shortcuts import render
from Customers.models import Customer,CustomerReport
from Setupboxes.models import SetupBox
from Collections.models import CollectedCustomer,Collection
import datetime
# Create your views here.

def DashboardView(request):
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


def SetupBoxes(request):
    setupbox = SetupBox.objects.all()
    active = setupbox.filter(box_status='active').count()
    unactive = setupbox.filter(box_status='deactive').count()
    context = {
        'setupbox':setupbox,
        'activecount':active,
        'unactivecount':unactive
    }
    return render(request,'Dashboard/setupbox.html',context)


def Collected_Customers(request):
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        coll = CollectedCustomer.objects.filter(collected_date=date)
    except TypeError:
        pass
    total_collection = 0
    for c in coll:
        total_collection+=c.collected_amount
       

    context = {
        "total_collection":total_collection,
        "collected_customers":coll,
    }
    return render(request,'Dashboard/collected_customers.html',context)

def CollectionView(request):
    coll = Collection.objects.all()
    context = {
        "collection":coll
    }
    return render(request,'Dashboard/collection.html',context)


def CustomerPaymentReports(request):
    cpr = CustomerReport.objects.all()
    cprcount = cpr.count() 
    context = {
        'cpr':cpr,
        'cprcount':cprcount
    }
    return render(request,'Dashboard/customer_report.html',context)