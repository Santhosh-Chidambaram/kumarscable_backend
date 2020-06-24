from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin




@admin.register(CollectedCustomer)
class CollectedCustomerAdminAll(ImportExportModelAdmin):
    list_display = ('collection_agent','customer','street','collected_amount','collected_date','month')
    ordering = ['collected_date']
    list_filter = ['collected_date','street']
    search_fields=('collected_date','street','collected_amount','customer')
    date_hierarchy = 'collected_date'
    list_per_page = 250
    readonly_fields = ['month','collected_date']
    
@admin.register(Collection)
class CollectionAdminAll(ImportExportModelAdmin):
    list_display = ('collection_agent','collection_amount', 'date',)
    ordering = ['date']
    list_filter = ['date','collection_agent']
    search_fields=('date','collection_amount')
    date_hierarchy = 'date'
    list_per_page = 250
    readonly_fields = ['date']