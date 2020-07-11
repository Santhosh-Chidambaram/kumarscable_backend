from django.urls import path
from .views import *

from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('api/getuserid',getUserId.as_view(),name="getuserid"),
    path('api-token-auth/',CustomAuthToken.as_view(),name='api_token_auth'),
    path('api/checkout/<int:pk>',CheckoutView,name="checkout"),
    path('api/customer/register',CustomerRegisterView,name="customerregister"),
    path('api/customerdata/<int:pk>',CustomerDataView),
    path('api/customer/packagerequest',PackageRequestView),
    path('api/customer/packagerequest/<int:id>',GetPackageRequestView),
    path('api/customer/addstb/<str:boxno>',addSTBView),
    path('api/customer/complaint',RegisterCompaint.as_view()),


    path('api/customers',CustomerList.as_view(),name='api-customers'),
    path('api/packages',PackagesListView,name='api-packages'),
    path('api/channels',ChannelsListView,name='api-channels'),
    path('api/customer-details/<str:boxno>',GetCustomer.as_view(),name='api-getcsdetail'),
    path('api/customers/<int:pk>',CustomerDetail,name='api-customerdetail'),
    path('api/customer/payment/update/<int:pk>',CustomerPaymentUpdate,name='api-cspaymentupdate'),
    path('api/setalltounpaid',setAllCustomersToUnpaid,name='setalltounpaid'),
    path('api/shareamount/',ShareAmountView,name="shareamount"),
    path('api/listcustomers',ListCustomers.as_view(),name="cus-list")
]