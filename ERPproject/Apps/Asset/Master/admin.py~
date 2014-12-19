from django.contrib import admin
from django import forms
from Apps.Asset.Master.models import *
from suit.widgets import SuitSplitDateTimeWidget, AutosizedTextarea, EnclosedInput
#from mptt.models import Category
from django.contrib.auth.models import Group
from Apps.Hrm.Master_General.models import *
from Apps.Distribution.master_sales.models import *
#from mptt.admin import MPTTModelAdmin
#from suit.admin import SortableModelAdmin


class Ms_asset_adminForm(forms.ModelForm):
    class Meta:
        model = Ms_asset
        widgets = {
            'life_time': EnclosedInput(append='thn', attrs={'class': 'input-medium'}),
            'price': EnclosedInput( prepend='Rp.', attrs={'class': 'input-medium'}),
            'salvage': EnclosedInput( prepend='Rp.', attrs={'class': 'input-medium'}),
            }

#class Ms_asset_admin(MPTTModelAdmin, SortableModelAdmin):
class Ms_asset_admin(admin.ModelAdmin):
    #mptt_level_indent = 20
    list_display = ['ID','asset_name','add_date','type','location','department','price', 'jadwal_maintenance','nilai_sisa_asset','nilai_penyusutan','coba',]
    search_fields = ['ID','asset_name','location','type','usage_status',]
    list_filter = ['add_date','status_loan',]
    date_hierarchy = 'add_date'
    list_per_page = 10
    form = Ms_asset_adminForm
    #list_display_links = ('ID',)
    #sortable = 'order'
    """
        def ID(self):
            return ' %(no_reg)s | %(asset_name)s' % {'no_reg':self.no_reg,'asset_name':self.asset_name}
        ID.short_description='Plat Number'
    """
    def suit_row_attributes(self, obj, request):
        css_class = {
            2: 'info',}.get(obj.status_loan)
        if css_class:
            return {'class': css_class, 'data': obj.status_loan}

    def suit_row_attributes(self, obj, request):
        css_class = {
            2: 'warning',}.get(obj.maintenance_status)
        if css_class:
            return {'class': css_class, 'data': obj.maintenance_status}


            #def queryset(self, request, obj=None):
            #	data = Ms_asset.objects.filter(usage_status = 1)
            #	return data

            #def save_model(self, request, Ms_asset,form,change):
            #	dep = Group.objects.get(user=request.user)
            #	if dep.name == 'unit':
            #		Ms_asset.department = dep.department
            #	Ms_asset.save()

            #dibuat menampilkan data waktu pertaman muncul
    def queryset(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        user2 = StaffPerson.objects.get(user=request.user)
        data = Ms_asset.objects.filter(usage_status = 1)
        if user.name=='unit':
            return Ms_asset.objects.filter(department=user2.employee.department, usage_status = 1)
        elif user.name=='staff':
            return data
        elif request.user.is_superuser:
            return Ms_asset.objects.all()


    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'unit':
            readonly_fields += ('ID','asset_name','add_date','freq_m','type','end_warranty','department','location','condition','price','life_time','salvage','jadwal_maintenance','nilai_sisa_asset','status_loan','usage_status','maintenance_status',)

        elif data.name == 'staff':
            if getattr(obj, 'ID', None) != None:
                readonly_fields += ('ID','asset_name','add_date','freq_m','type','end_warranty','department','location','condition','price','life_time','salvage','jadwal_maintenance','nilai_sisa_asset','status_loan','usage_status','maintenance_status',)

        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

admin.site.register(Ms_asset, Ms_asset_admin)

class Historical_asset_admin(admin.ModelAdmin):
    list_display = ['no_reg','asset_name','add_date','type','department','disposal_date']
    search_fields = ['no_reg','asset_name','type','disposal_date']
    list_filter = ['disposal_date','department',]

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'unit':
            readonly_fields += ('no_reg','asset_name','add_date','type','department','disposal_date',)
        else:
            readonly_fields +=('no_reg','asset_name','add_date','type','department','disposal_date',)
        return readonly_fields

admin.site.register(Historical_asset, Historical_asset_admin)
"""
class Category_admin(MPTTModelAdmin, SortableModelAdmin):
	list_display = ['name', 'slug', 'is_active']
	list_editable = ['is_active']

admin.site.register(Category, Category_admin)
"""



