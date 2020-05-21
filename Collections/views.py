from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import CollectedCustomer,Collection
from rest_framework.decorators import api_view,permission_classes
from rest_framework.mixins import ListModelMixin
from .serializers import CollectedCustomerSerializer,CollectionSerialzer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User
import json
import datetime
from django.shortcuts import get_object_or_404,get_list_or_404




@api_view(['POST'])
def CollectionAmountView(request):
    
    if request.method == 'POST':
        serializer =CollectionSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Collection Api View

class CollectedCustomers(APIView):
    def post(self,request):

        serializer = CollectedCustomerSerializer(data=request.data)
        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        collected = CollectedCustomer.objects.filter(collected_date=date)
        return Response({
            "id":coll.id,
            "collector":coll.collector.id,
            "customer_name":coll.customer.name,
            "collected_date":coll.collected_date,
            "collected_amount":coll.collected_amount,
            "street":coll.customer.street,

        } for coll in collected )

@api_view(['GET'])
def cccount(request):
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    coll_cus = CollectedCustomer.objects.filter(collected_date=date)
    return Response({
        "cccount":coll_cus.count()
    })



class CollectionReports(APIView):
    
    def post(self,request):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        coll_cus = CollectedCustomer.objects.filter(collected_date=date)
        collection = Collection.objects.filter(date=date) 
        total_collection = 0
        collection_customers  = []
        collected_date = date
        latest_collection_list = []
        if collection.first():
            for coll in collection:
                for c in coll.collection_list.all():
                    latest_collection_list.append(c.id)
        for coll in coll_cus:
            if latest_collection_list:
                if not coll.customer.id in latest_collection_list:
                    total_collection+=coll.collected_amount
                    collection_customers.append(coll.customer.id) 

            else:
                    total_collection+=coll.collected_amount
                    collection_customers.append(coll.customer.id)
 
        data1 ={
            "collector":1,
            "collection_amount":total_collection,
            "date":str(collected_date),
            "collection_list":collection_customers
        }
        collection_customers=[]
        serializer = CollectionSerialzer(data = data1)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"Customers list empty"},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        try:
            coll = Collection.objects.filter(date=date)
        except TypeError:
            return Response({"Object not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({
            "date":c.date,
            "collection_list":[{"customer_name":cc.name,"paid_amount":cc.payment_amount,"payment_status":cc.payment_status}for cc in c.collection_list.all()],
            "collection_amount":c.collection_amount,
            "collector":c.collector.id

        }for c in coll)


@api_view(['GET'])
def totalCollection(request):
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        coll = Collection.objects.filter(date=date)
    except TypeError:
        return Response({"Object not found"},status=status.HTTP_404_NOT_FOUND)
    total_collection = 0
    total_customer = []
    for c in coll:
        tc={}
        total_collection+=c.collection_amount
        for cc in c.collection_list.all():
            tc={"customer_name":cc.name,"paid_amount":cc.payment_amount,"payment_status":cc.payment_status}
            total_customer.append(tc)


    return Response({
        "total_collection":total_collection,
        "total_customers":total_customer,
    })