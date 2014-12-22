from django.contrib import admin
from Apps.Manufacturing.ProductionExecution.models import *
"""
class out_productionAdmin(admin.ModelAdmin):
	list_display = ['speed_out','eff_out','order_out','broken_out','weight_out','add_date_time',]
	list_filter = ['speed_out',]
	search_filter = ['speed_out',]
admin.site.register(out_production, out_productionAdmin)
"""
class production_recordAdmin(admin.ModelAdmin):
#	list_display = ['Production_Plans','Out_Production',]
	list_display = ['Production_Plans','speed_out','eff_out','order_out','broken_out','weight_out','add_date_time',]
	list_filter = ['Production_Plans',]
	search_filter = ['Production_Plans',]
admin.site.register(production_record, production_recordAdmin)

class Use_ResourcesAdmin(admin.ModelAdmin): 
	list_display = ['Production_Plans','Issue_Material','Machine_Usage','add_date_time',] #	list_display = ['speed_out','eff_out','order_out','broken_out','add_date_time',]
	list_filter = ['Production_Plans',]
	search_filter = ['Production_Plans',]
admin.site.register(Use_Resources, Use_ResourcesAdmin)

class Inspection_ProductsAdmin(admin.ModelAdmin):
	list_display = ['Production_Plans','Dimension_Diameter','Dimension_Height','Volume','Physics',]
	list_filter = ['Production_Plans',]
	search_filter = ['Production_Plans',]
admin.site.register(Inspection_Products, Inspection_ProductsAdmin)