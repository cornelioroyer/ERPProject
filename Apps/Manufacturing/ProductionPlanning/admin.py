from django.contrib import admin
from Apps.Manufacturing.ProductionPlanning.models import *
from Apps.Manufacturing.Manufacturing.models import *
from Apps.Manufacturing.MasterData.models import *
from Apps.Manufacturing.const import *


class Master_ProductAdmin(admin.ModelAdmin):
#	list_display = ['Product_Id','Product_Name','Description','Optimistic_Time','EML_Time','Pesseimistic_Time','speeds','Dimension_Diameter','Dimension_Height','Volume','Physics','Product_Design','Product_Label',]
#	list_display = ['no_reg','Product_Name','Description','Speed','Dimension_Diameter','Dimension_Height','Volume','Physics','Product_Design','Product_Label',]
	list_display = ['no_reg','Product_Name','products_reviewx','Dimension_Diameter','Dimension_Height','Volume','Physics','Product_Design','Product_Label',]
	list_filter = ['Product_Name',]
	search_filter = ['Product_Name',]
admin.site.register(Master_Product, Master_ProductAdmin)

class Master_BoMAdmin(admin.ModelAdmin):
	list_display = ['no_reg','ManufacturingOrder','Add_Date',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
admin.site.register(Master_BoM, Master_BoMAdmin)

"""
class Production_MechineAdmin(admin.ModelAdmin):
	list_display = ['MC_Production','Current_Status',]
	list_filter = ['MC_Production',]
	search_filter = ['MC_Production',]
admin.site.register(Production_Mechine, Production_MechineAdmin)


class ACL_MechineAdmin(admin.ModelAdmin):
	list_display = ['Acl_Production',]
	list_filter = ['Acl_Production',]
	search_filter = ['Acl_Production',]
admin.site.register(ACL_Mechine, ACL_MechineAdmin)


class CartonAdmin(admin.ModelAdmin):
	list_display = ['Carton_Type','Carton_Quantity','Add_Time_Date',]
	list_filter = ['Carton_Type',]
	search_filter = ['Carton_Type',]
admin.site.register(Carton, CartonAdmin)

class Packing_PlanningAdmin(admin.ModelAdmin):
	list_display = ['Carton','Plastic_Quantity','Forklift_Quantity','Line_Quantity','BlowTorch_Quantity','Add_Time_Date',]
	list_filter = ['Carton',]
	search_display = ['Carton',]
admin.site.register(Packing_Planning, Packing_PlanningAdmin)

class Master_TeamAdmin(admin.ModelAdmin):
	list_display = ['Team_Name','Initial_Team','Description_Material',]
	list_filter = ['Team_Name',]
	search_filter = ['Team_Name',]
admin.site.register(Master_Team, Master_TeamAdmin)

class rkap_productionAdmin(admin.ModelAdmin):		# rkap (rencana kapasitas & jadwal produksi)
	list_display = ['rkap_id','speed_in','eff_in','order_in','weight_in','add_date_time',]
	list_filter = ['rkap_id',]
	search_filter = ['rkap_id',]
admin.site.register(rkap_production, rkap_productionAdmin)
"""	
class production_plansAdmin(admin.ModelAdmin):
#	list_display = ['Job_Num','M_O','Start_Date','End_Date','Durasi','MC_P','Product_Quantity_PerMC','xx','Master_BoM',]
	list_display = ['no_reg','M_O','Start_Date','End_Date','Durasi','MC_P','Product_Quantity_PerMC','Master_BoM','cetak',]
	list_filter = ['no_reg',]
	search_filter = ['no_reg',]
	exclude = ['Start_Date','End_Date','MC_P','Product_Quantity_PerMC',]
admin.site.register(production_plans, production_plansAdmin)


class Bill_Of_MaterialAdmin(admin.ModelAdmin):
	list_display = ['Master_BoM','Master_Material','Material_Quantity','Unit_Measure','materials',]
	list_filter = ['Master_BoM',]
	search_filter = ['Master_BoM',]
admin.site.register(Bill_Of_Material, Bill_Of_MaterialAdmin)
"""
class ACL_MechineAdmin(admin.ModelAdmin):
	list_display = ['Acl_Production','Current_Status',]
	list_filter = ['Acl_Production',]
	search_filter = ['Acl_Production',]
admin.site.register(ACL_Mechine, ACL_MechineAdmin)

class label_plansAdmin(admin.ModelAdmin):
	list_display = ['Job_Num','M_O','Start_Date','End_Date','Durasi','Label_Cat','ACL_M','Team_Work',]
	list_filter = ['Job_Num',]
	search_filter = ['Job_Num',]
admin.site.register(label_plans, label_plansAdmin)

class nyoba_calenderAdmin(admin.ModelAdmin):
	list_display = ['test',]
	list_filter = ['test',]
	search_filter = ['test',]
admin.site.register(nyoba_calender, nyoba_calenderAdmin)
"""
