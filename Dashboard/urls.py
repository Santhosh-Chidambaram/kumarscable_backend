from django.urls import path
from .views import *




urlpatterns = [
    path('adminuser/dashboard/',DashboardView,name='kc_admin_dashboard'),
    path('adminuser/setupboxes/',SetupBoxes,name='kc_setupboxes'),
    path('adminuser/collected/customers/',Collected_Customers,name='kc_ccustomers'),
    path('adminuser/customers/reports/',CustomerPaymentReports,name='kc_customerreports'),
    path('adminuser/collections/reports/',CollectionView,name='kc_collectionreports'),
    
]