""" @author: Rhiyananta Catur Yudowicitro """


from django.contrib import admin
from Apps.Inventory.Inventory_Intelligh_Location_Assigment.models import Header_commodity, data_commodity,Header_commodity_Material, data_commodity_Material

class Header_commodityAdmin (admin.ModelAdmin):
    list_display = ('name_warehouse', 'lock', 'date_now')
    search_field = ['name_warehouse', 'lock']
    
admin.site.register(Header_commodity, Header_commodityAdmin)


class data_commodityAdmin (admin.ModelAdmin):
    list_display = ('header','name_commodity','type','quantity','unit','saved_location')
    search_field = ['name_commodity', 'quantity']
    
    def get_form(self, request, object=None, **kwargs):
        form = super(data_commodityAdmin, self).get_form(request, object, **kwargs)
        xx = False
        try:
            x = getattr(object, 'header', None)
            xx = x.lock
        except: pass
        
        if xx == False:
            form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(lock=False)
        else:
            readonly_fields = ('header','name_commodity','type','quantity','unit','saved_location')
        return form 
    
admin.site.register(data_commodity, data_commodityAdmin)


class Header_commodity_MaterialAdmin (admin.ModelAdmin):
    list_display = ('name_warehouse', 'lock', 'date_now')
    search_field = ['name_warehouse', 'lock']
    
admin.site.register(Header_commodity_Material, Header_commodity_MaterialAdmin)


class data_commodity_MaterialAdmin (admin.ModelAdmin):
    list_display = ('header','name_commodity','type','quantity','unit','saved_location')
    search_field = ['name_commodity', 'quantity']
    
    def get_form(self, request, object=None, **kwargs):
        form = super(data_commodity_MaterialAdmin, self).get_form(request, object, **kwargs)
        xx = False
        try:
            x = getattr(object, 'header', None)
            xx = x.lock
        except: pass
        
        if xx == False:
            form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(lock=False)
        else:
            readonly_fields = ('header','name_commodity','type','quantity','unit','saved_location')
        return form 
    
admin.site.register(data_commodity_Material, data_commodity_MaterialAdmin)
