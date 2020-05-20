from django.urls import path
from .views import *





urlpatterns = [
     path('api/customers',CustomerList.as_view(),name='api-customers'),
    path('api/customer-details/<str:boxno>',GetCustomer.as_view(),name='api-getcsdetail'),
    path('api/customers/count',customersCount,name='api-customerscount'),
    path('api/customers/<int:pk>',CustomerDetail,name='api-customerdetail'),
    path('api/customer/payment/update/<int:pk>',CustomerPaymentUpdate,name='api-cspaymentupdate'),
    path('api/setalltounpaid',setAllCustomersToUnpaid,name='setalltounpaid'),
]