from django.urls import path
from .views import ChannelList,PackagesList,STBList,stbsCount,STBDetail


urlpatterns = [
    path('api/channels',ChannelList.as_view(),name='api-channels'),
    path('api/packages',PackagesList.as_view(),name='api-packages'),
    path('api/stbs',STBList.as_view(),name='api-stbs'),
    path('api/stbs/count',stbsCount,name='api-stbscount'),
    path('api/stbs/<int:pk>',STBDetail,name="api-stbsdetail"),
    
]