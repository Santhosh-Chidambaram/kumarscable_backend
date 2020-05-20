from django.contrib import admin
from .models import Channel,Bouquet,BroadcastBouquet,SetupBox
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Channel)
class ChannelAdminAll(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields=('id','name')
    ordering = ['id']

@admin.register(Bouquet)
class BouquetAdminAll(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price')
    ordering = ['id']

@admin.register(BroadcastBouquet)
class BcbouquetAdminAll(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price')
    ordering = ['id']

@admin.register(SetupBox)
class SetupBoxAdmin(ImportExportModelAdmin):
    list_filter=['box_status']
    list_display=('id','boxno','base_package','box_status','start_date','end_date')
    search_fields=('boxno','box_status')
    ordering = ['id']
    list_per_page = 250
    fieldsets=(
        ('Box Details',{
            'fields':('boxno','base_package',
            'end_date','base_price',
            'additional_price','gst_price','total_price')
        }),
        ('Subscriptions',{
            'fields':('addon_packages','bouquets','broadcast_bouquets')
        }),
        ('Activation',{
            'fields':('box_status','deactive_reason')
        })
    )
