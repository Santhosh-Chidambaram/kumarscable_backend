from django.urls import path
from .views import *




urlpatterns = [
    path('',HomeView,name='kc_home'),
    path('login/',LoginView.as_view(),name='user_login'),
    path('adminuser/dashboard/',DashboardView.as_view(),name='kc_admin_dashboard'),
    path('adminuser/collected/customers/',Collected_Customers,name='kc_ccustomers'),
    path('adminuser/customers/reports/',CustomerPaymentReports,name='kc_customerreports'),
    path('adminuser/collections/reports/',CollectionView,name='kc_collectionreports'),
    path('adminuser/collections/reports/<int:pk>/customers/',CollectionListView,name='kc_collectioncuslist'),
    path('adminuser/customers/',CustomerStatusView,name='kc_customerstatus'),
    
]