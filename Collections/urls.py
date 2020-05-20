from django.urls import path
from .views import CollectionAmountView, CollectedCustomers, CollectionReports, cccount, totalCollection



urlpatterns = [
    path('api/collection/update', CollectionAmountView, name='collectionupdate'),
    path('api/collectedcustomers', CollectedCustomers.as_view(),
         name='collected_customers'),
    path('api/collectionreports/', CollectionReports.as_view(),
         name='collectionreports'),
    path('api/collectedcustomers/count', cccount, name='cccount'),
    path('api/totalcollection', totalCollection, name='totalCollection'),

]
