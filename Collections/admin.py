from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin




@admin.register(CollectedCustomer)
class CollectedCustomerAdminAll(ImportExportModelAdmin):
    list_display = ('customer', 'collected_date','street','collected_amount')
    ordering = ['collected_date']
    list_filter = ['collected_date','street']
    search_fields=('collected_date','street','collected_amount')
    date_hierarchy = 'collected_date'
    list_per_page = 250
    readonly_fields = ['month','collected_date']
    
@admin.register(Collection)
class CollectionrAdminAll(ImportExportModelAdmin):
    list_display = ('collector', 'date','collection_amount')
    ordering = ['date']
    list_filter = ['date','collector']
    search_fields=('date','collection_amount')
    date_hierarchy = 'date'
    list_per_page = 250
    readonly_fields = ['date']