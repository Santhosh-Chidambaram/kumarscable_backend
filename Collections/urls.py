from django.urls import path
from .views import  CollectedCustomers, CollectionReports, totalCollection



urlpatterns = [
   
    path('api/collectedcustomers', CollectedCustomers.as_view(),
         name='collected_customers'),
    path('api/collectionreports/', CollectionReports.as_view(),
         name='collectionreports'),
    path('api/totalcollection', totalCollection, name='totalCollection'),

]
