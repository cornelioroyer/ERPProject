from django.contrib import admin
from Apps.Inventory.Inventory_Lost_Control.models import *
#from Apps.Inventory.Inventory_Lost_Control.models import Control_warehouse, needs_commodity, Control_warehouse_material
                    
class Control_warehouseAdmin (admin.ModelAdmin): 
    list_display = ('warehouse_name','commodity','category','date','unit','total_commodity','description')
    search_field =['warehouse_name']
    
admin.site.register(Control_warehouse, Control_warehouseAdmin)

class needs_commodityAdmin (admin.ModelAdmin):
    list_display = ('number_needs','name_commodity','commodity_code','date','unit','total_request','stock','total_purchase','description')
    list_filter = ('name_commodity',)
    search_field = ('name_commodity')
    
admin.site.register(needs_commodity, needs_commodityAdmin)

class Control_warehouse_materialAdmin (admin.ModelAdmin): 
    list_display = ('warehouse_name','commodity','category','date','unit','total_commodity','description')
    search_field =['warehouse_name']
    
admin.site.register(Control_warehouse_material, Control_warehouse_materialAdmin)
