from django.contrib import admin
from Apps.Asset.Penggantian.models import *
from Apps.Asset.Request.models import *
from django.contrib.auth.models import Group
from Apps.Distribution.master_sales.models import *

#class Header_change_requestInline(admin.TabularInline):
#	model = Header_change_request
class DataChangeInline(admin.TabularInline):
	model = Data_change_request
	extra = 1
	max_num = 0
	can_delete = True
	
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			if getattr(obj, 'header', None) != None:
				readonly_fields = ('header',)
			else :
				readonly_fields = ('asset','request','description','change_status', )
		else: 
			readonly_fields = ('header','asset','request','description','change_status',)
		
		return readonly_fields
		
class Header_change_request_admin(admin.ModelAdmin):
	list_display = ['no_reg','department','change_date','asset_staff_review','department_staff_review','department_staff_aggrement']
	search_fields = ['no_reg','department','change_date']
	inlines = [DataChangeInline,]
	list_filter = ['department','change_date','department_staff_aggrement']
	
	
	def save_model(self, request, Header_change_request,form,change):
		dep = Group.objects.get(user=request.user)
		dep2 = StaffPerson.objects.get(user=request.user)
		if dep.name == 'unit':
			Header_change_request.department = dep2.employee.department
		Header_change_request.save()
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		data = Ms_asset.objects.filter(usage_status = 1)
		if user.name=='unit':
			return Header_change_request.objects.filter(department=user2.employee.department)
		else :
			return Header_change_request.objects.all()	
			
		if request.user.is_superuser:
			return Header_change_request.objects.all()
	
		
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			readonly_fields += ('no_reg','department','change_date','asset_staff_review',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields += ('department_staff_aggrement','department_staff_review',)
			else:
				readonly_fields = ('no_reg','department','change_date','asset_staff_review',)
		elif data.name == 'staff':
			readonly_fields = ('department_staff_review','department_staff_aggrement',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields +=('department','asset_staff_review',)
			else :
				readonly_fields =('department_staff_review','department_staff_aggrement',)
		return readonly_fields

admin.site.register(Header_change_request, Header_change_request_admin)

class Data_change_request_admin(admin.ModelAdmin):
	list_display = ['header','asset','request','change_status','descriptionx']
	search_fields = ['header','asset','change_status']
	list_filter = ['request','change_status',]
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		if user.name=='unit':
			return Data_change_request.objects.filter(header__department=user2.employee.department)
		else :
			return Data_change_request.objects.all()	
			
		if request.user.is_superuser:
			return Data_change_request.objects.all()
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Data_change_request_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			x = getattr(obj, 'header', None)
			xx = True
			if getattr(obj, 'header', None) == None:
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
				self.exclude = ['description',]
			else :
				if getattr(obj, 'header', None) != None:
					if x.department_staff_aggrement == False:
						form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.department,usage_status=1)
						form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service=13)
					else :
						self.exclude = ['description',]
			
		else :
			readonly_fields = ['header','asset','request','change_status','descriptionx',]
			self.exclude = ['description',]
		return form
		
		"""
			xx = False
			try:
				x = getattr(obj,'header', None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == False:
				form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service__startswith = 13)#jaga2 untuk permintaan penggantian
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
		else :
			readonly_fields = ('header','asset','request','change_status','description',)
		return form
		"""
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			if getattr(obj, 'header', None) == None:
				readonly_fields = ('asset','request','change_status','descriptionx',)
			else :
				readonly_fields = ('header',)
			xx = False
			try:
				x = getattr(obj, 'header', None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == False:
				readonly_fields += ()
			else: 
				readonly_fields += ('asset','request','change_status','descriptionx',)
				
		elif data.name == 'unit':
			if getattr(obj, 'header', None) != None:
				readonly_fields = ('header','asset','request','change_status','descriptionx',)
			else :
				readonly_fields = ('header',)
				
			xx = False
			try:
				x = getattr(obj,'header',None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == True:
				readonly_fields = ('header','asset','request','change_status','descriptionx',)
			else :
				readonly_fields = ('header','asset','request','change_status','descriptionx',)
		
		return readonly_fields
	"""
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
				xx = False
				try:
					x = getattr(obj,'header',None)
					xx = x.department_staff_aggrement
				except: pass
				if xx == True:
					readonly_fields += ('header','asset','request','change_status','description',)
				else: 
					readonly_fields = ()
		else: 
			readonly_fields = ('header','asset','request','description','change_status',)
		
		return readonly_fields
	"""
admin.site.register(Data_change_request, Data_change_request_admin)


class Data_request_asset_change_admin(admin.ModelAdmin):
	list_display = ['header_asset','title','detailx','ra_used','ra_amount','send_request',]
	search_fields = ['header_asset']
#	inlines = [Header_change_request,]
	"""	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Data_request_asset_change_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			x = getattr(obj, 'header_asset', None)
			if getattr(obj, 'header_asset', None) == None:
				form.base_fields['header_asset'].queryset = form.base_fields['header_asset'].queryset.filter(department_staff_aggrement=True)
			else: 
				pass
		return form
	"""
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Data_request_asset_change_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			xx = False
			try:
				x = getattr(obj, 'header_asset', None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == False:
				form.base_fields['header_asset'].queryset = form.base_fields['header_asset'].queryset.filter(department_staff_aggrement=True)
			else :
				readonly_fields = ()
		else:
			readonly_fields = ('header_asset','title','detailx','ra_used','ra_amount','send_request',)
		return form
		
admin.site.register(Data_request_asset_change, Data_request_asset_change_admin)




