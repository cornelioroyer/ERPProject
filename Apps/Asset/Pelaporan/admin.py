from django.contrib import admin
from Apps.Asset.Pelaporan.models import *

class Header_asset_report_admin(admin.ModelAdmin):
	list_display = ['no_reg','report_add_date','asset_manager_aggrement']
	search_fields = ['report_add_date']

admin.site.register(Header_asset_report, Header_asset_report_admin)

class Data_asset_report_admin(admin.ModelAdmin):
	list_display = ['header','choice','start_month','until_month']
	search_fields = ['header']

admin.site.register(Data_asset_report, Data_asset_report_admin)
