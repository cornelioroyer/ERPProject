from django.contrib import admin
from Apps.Asset.Maintenance.models import *
from django.contrib.auth.models import Group
from Apps.Distribution.master_sales.models import *

class DataRMInline(admin.TabularInline):
	model = Data_maintenance_asset
	extra = 1
	max_num = 0
	can_delete = True
	readonly_fields = ('header_maintenance','user_request','asset','maintenance_type','rm_used','estimation','description','cost_estimate',)

"""
class Maintenance_type_admin(admin.ModelAdmin):
	list_display = ['maintenance_type']
	search_fields = ['maintenance_type']

admin.site.register(Maintenance_type, Maintenance_type_admin)
"""

class Header_maintenance_asset_admin(admin.ModelAdmin):
	list_display = ['no_reg','department','rm_add_date','asset_staff_review','rm_lock','maintenance_status','finished_status',]
	search_fields = ['maintenance_status','no_reg','department','rm_month']
	inlines = [DataRMInline,]
	
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		data = Ms_asset.objects.filter(usage_status = 1)
		if user.name=='unit':
			return Header_maintenance_asset.objects.filter(department=user2.employee.department)
		else :
			return Header_maintenance_asset.objects.all()	
			
		if request.user.is_superuser:
			return Header_maintenance_asset.objects.all()
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Header_maintenance_asset_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'unit':
			self.exclude = ['finished_status',]
			
		else : 
			self.exclude = []
		
		return form
	
	#def queryset(self, request, obj=None):
	#	user = Role_user_asset.objects.get(user=request.user)
	#	data = Ms_asset.objects.filter(usage_status = 1)
	#	if user.access_level=='unit':
	#		return Header_maintenance_asset.objects.filter(department=user.department, usage_status = 1)
	#	elif user.access_level=='staff':
	#		return 				
	#	if request.user.is_superuser:
	#		return Header_maintenance_asset.objects.all()

	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			readonly_fields += ('no_reg','department','rm_lock_date','maintenance_status','asset_staff_review','finished_status',)
			if getattr(obj, 'rm_lock', None) == True:
				readonly_fields += ('rm_lock',)
		elif data.name == 'staff':
			readonly_fields += ('rm_lock',)
			if getattr(obj, 'rm_lock',None) == True:
				readonly_fields += ('no_reg','department','rm_lock_date','maintenance_status','asset_staff_review',)
		return readonly_fields
			

admin.site.register(Header_maintenance_asset, Header_maintenance_asset_admin)



class Data_maintenance_asset_admin(admin.ModelAdmin):
	list_display = ['header_maintenance','user_request','asset','maintenance_type','estimation','cost_estimate']
	search_fields = ['user_request','maintenance_type','asset']
	list_filter = ['maintenance_type','asset']
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		if user.name=='unit':
			return Data_maintenance_asset.objects.filter(header_maintenance__department=user2.employee.department, asset__usage_status = 1)
		elif user.name=='staff':
			return Data_maintenance_asset.objects.all()				
		if request.user.is_superuser:
			return Data_maintenance_asset.objects.all()
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Data_maintenance_asset_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			x = getattr(obj, 'header_maintenance', None)
			xx = True
			if getattr(obj, 'header_maintenance', None) == None:
				form.base_fields['header_maintenance'].queryset = form.base_fields['header_maintenance'].queryset.filter(rm_lock=False)
			else :
				if getattr(obj, 'header_maintenance', None) != None:
					if x.rm_lock == False:
						form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.department)
						form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(usage_status=1)
						form.base_fields['user_request'].queryset = form.base_fields['user_request'].queryset.filter(answer_service=2)
						
		else:
			readonly_fields = ('header_maintenance','user_request','asset','maintenance_type','estimation','cost_estimate',)
		
				
		return form
		
		"""	
			xx = False
			try:
				x = getattr(obj,'header_maintenance', None)
				xx = x.rm_lock
			except: pass
			if xx == False:
				form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.department)
				form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(usage_status=1)
				form.base_fields['user_request'].queryset = form.base_fields['user_request'].queryset.filter(answer_service=2)
				form.base_fields['header_maintenance'].queryset = form.base_fields['header_maintenance'].queryset.filter(rm_lock=False)
							
			else: 
				readonly_fields = ('header_maintenance','user_request','asset','maintenance_type','estimation','cost_estimate',)
		return form
	
	def get_form(self, request, obj=None, **kwargs):
		data = Role_user_asset.objects.get(user=request.user)
		form = super(Data_loaning_request_admin, self).get_form(request, obj, **kwargs)
		if data.access_level == 'staff':
			x = getattr(obj, 'header', None)
			xx = True
			if getattr(obj, 'header', None) == None:
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
			else :						
				if getattr(obj, 'header', None) != None:
					if x.department_staff_aggrement == False:
						form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.from_department,usage_status=1)
						form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service=5)
					
		else:
			readonly_fields = ('header','request','asset','description',)
		
				
		return form
	
	"""
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			if getattr(obj, 'header_maintenance', None) == None:
				readonly_fields = ('user_request','asset','maintenance_type','estimation','cost_estimate','description','rm_used',)
			else :
				readonly_fields = ('header_maintenance',)
			xx = False
			try:
				x = getattr(obj, 'header_maintenance', None)
				xx = x.rm_lock
			except: pass
			if xx == False:
				readonly_fields += ()
			else: 
				readonly_fields = ('header_maintenance','user_request','asset','maintenance_type','estimation','cost_estimate','description','rm_used',)
				
		elif data.name == 'unit':
			if getattr(obj, 'header_maintenance', None) != None:
				readonly_fields = ('header_maintenance','user_request','asset','maintenance_type','estimation','cost_estimate','rm_used','description',)
			else :
				readonly_fields = ('header_maintenance',)
				
			xx = False
			try:
				x = getattr(obj,'header_request',None)
				xx = x.rm_lock
			except: pass
			if xx == True:
				readonly_fields += ('header_maintenance','user_request','asset','maintenance_type','estimation','cost_estimate',)
			else :
				readonly_fields +=()
		
		return readonly_fields
		
	"""
	def get_readonly_fields(self, request, obj=None):
		data = Role_user_asset.objects.get(user=request.user)
		readonly_fields = ()
		if data.access_level == 'staff':
			xx = False
			try:
				x = getattr(obj, 'header_maintenance', None)
				xx = x.rm_lock
			except: pass
			if xx == True:
				readonly_fields = ('header_maintenance','user_request','asset','maintenance_type','estimation','description','rm_used','cost_estimate',)
			else: 
				readonly_fields = ()
				
		elif data.access_level == 'unit':
			readonly_fields += ('header_maintenance','user_request','asset','maintenance_type','estimation','description','rm_used','cost_estimate',)

		return readonly_fields	
	"""		
admin.site.register(Data_maintenance_asset, Data_maintenance_asset_admin)

#class Data_maintenance_schedule_admin(admin.ModelAdmin):
#	list_display = ['department','msc_date','month_of_maintenance','Dept_staff_review']
#	search_fields = ['department','asset_salvage','month_of_maintenance']

#admin.site.register(Data_maintenance_schedule, Data_maintenance_schedule_admin)
