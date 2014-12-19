from django.contrib import admin
from Apps.Inventory.Inventory_Planing.models import *
#from Apps.Inventory.Inventory_Planing.models import in_commodity, out_commodity, Warehouse_material


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehouse_name','code_warehouse','type_warehouse','description','unit','capacity_warehouse', 'available_capacity_warehouse')
    search_field = ['warehouse_name']
    
admin.site.register(Warehouse, WarehouseAdmin)


class in_commodityAdmin (admin.ModelAdmin):
    list_display = ('departemen_appelant','warehouse','name_item','type','quantity_commodity','date','satuan', 'total_item', 'description')
    search_field = ['warehouse']
    
admin.site.register(in_commodity, in_commodityAdmin)


class out_commodityAdmin (admin.ModelAdmin):
    list_display = ('departemen_appelant','warehouse','name_item','type','quantity_commodity','date','satuan','total_item', 'description')
    search_field = ['warehouse']
    
admin.site.register(out_commodity, out_commodityAdmin)


class Warehouse_materialAdmin(admin.ModelAdmin):
    list_display = ('warehouse_name','code_warehouse','type_warehouse','description','unit','capacity_warehouse', 'available_capacity_warehouse')
    search_field = ['warehouse_name']
    
admin.site.register(Warehouse_material, Warehouse_materialAdmin)

class in_commodity_materialAdmin (admin.ModelAdmin):
    list_display = ('departemen_appelant','warehouse','name_item','type','quantity_commodity','date','satuan', 'total_item', 'description')
    search_field = ['warehouse']
    
admin.site.register(in_commodity_material, in_commodity_materialAdmin)


class out_commodity_materialAdmin (admin.ModelAdmin):
    list_display = ('departemen_appelant','warehouse','name_item','type','quantity_commodity','date','satuan','total_item', 'description')
    search_field = ['warehouse']
    
admin.site.register(out_commodity_material, out_commodity_materialAdmin)

