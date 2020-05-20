from django.urls import path
from .views import *
from .api import *
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin

admin.site.site_header = "KUMARSCABLE ADMIN"
admin.site.site_title = "KUMARSCABLE ADMIN PORTAL"
admin.site.index_title = "WELCOME TO KUMARSCABLE ADMIN PORTAL"
urlpatterns = [
    path('',homeView,name='home'),
    path('contactus',ContactusView,name='contactus'),
    path('invoice',InvoiceView.as_view(),name='invoice'),
    path('api/getuserid',getUserId,name='getUserId'),




    #API URLS
    path('api-token-auth/',obtain_auth_token,name='api_token_auth'),
    path('api/invoice/<str:boxno>',InvoiceView.as_view(),name='api-invoice'),
    
    
    
    


    
]