from django.contrib import admin
from Apps.Asset.Penghapusan.models import *
from django.contrib.auth.models import Group
from Apps.Distribution.master_sales.models import *

class DataDisposalInline(admin.TabularInline):
	model = Data_disposal_request
	extra = 1
	max_num = 0
	can_delete = True
	readonly_fields = ('header','request','asset','description',)
	

class Disposal_status_admin(admin.ModelAdmin):
	list_display = ['disposal_status']
	search_fields = ['disposal_status']
	
admin.site.register(Disposal_status, Disposal_status_admin)

class Header_disposal_request_admin(admin.ModelAdmin):
	list_display = ['no_reg','department','disposal_date','asset_reviewx','dept_reviewx','department_staff_aggrement','disposal_status']
	search_fields = ['no_reg','department','disposal_date']
	inlines = [DataDisposalInline,]
	list_filter = ['disposal_date','disposal_status',]
	
	def save_model(self, request, Header_disposal_request,form,change):
		dep = Group.objects.get(user=request.user)
		dep2 = StaffPerson.objects.get(user=request.user)
		if dep.name == 'unit':
			Header_disposal_request.department = dep2.employee.department
		Header_disposal_request.save()
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		data = Ms_asset.objects.filter(usage_status = 1)
		if user.name=='unit':
			return Header_disposal_request.objects.filter(department=user2.employee.department)
		else :
			return Header_disposal_request.objects.all()	
			
		if request.user.is_superuser:
			return Header_disposal_request.objects.all()
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Header_disposal_request_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			x = getattr(obj, 'no_reg', None)
			xx = True
			if getattr(obj, 'no_reg', None) == None:
				self.exclude = ['department_staff_review',]	

			else: 
				if getattr(obj, 'department_staff_aggrement') == True:
					self.exclude = ['department_staff_review','asset_staff_review',]
		else : 
			x = getattr(obj, 'no_reg', None)
			xx = True
			if getattr(obj, 'no_reg', None) == None:
				self.exclude = ['department_staff_review',]	

			else: 
				if getattr(obj, 'department_staff_aggrement') == True:
					self.exclude = ['department_staff_review','asset_staff_review',]
				else: 
					self.exclude = ['asset_staff_review',]
					
		return form
	
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			readonly_fields += ('department','asset_reviewx','disposal_status',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields += ('department_staff_aggrement','dept_reviewx',)	 
		elif data.name == 'staff':
			readonly_fields += ('department_staff_aggrement','dept_reviewx',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields += ('department','asset_reviewx',)
			else:
				readonly_fields += ('disposal_status',)
			if getattr(obj, 'disposal_status', None) == True:
				readonly_fields += ('no_reg','department','disposal_date','asset_reviewx','disposal_status',)

		elif data.name == 'manager':
			readonly_fields = ()
		else :
			readonly_fields = ()
	#	elif data.name == 'manager' :
	#		readonly_fields = ()
		
		return readonly_fields
	
admin.site.register(Header_disposal_request, Header_disposal_request_admin)

class Data_disposal_request_admin(admin.ModelAdmin):
	list_display = ['header','request','asset','descriptionx']
	search_fields = ['header','asset']
	list_filter = ['request',]
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		if user.name=='unit':
			return Data_disposal_request.objects.filter(header__department=user2.employee.department)
		else :
			return Data_disposal_request.objects.all()	
			
		if request.user.is_superuser:
			return Data_disposal_request.objects.all()
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Data_disposal_request_admin, self).get_form(request, obj, **kwargs)
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
						form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service__startswith = 6)
					else:	
						self.exclude = ['description',]						
		else :
			readonly_fields = ('header','request','asset','descriptionx',)
			self.exclude = ['description',]	
		return form
		"""	
			xx = False
			try:
				x = getattr(obj,'header', None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == False:
				form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.department)
				form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(usage_status= 1)
				form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service__startswith = 6)
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
			else:
				readonly_fields = ()
		else :
			readonly_fields = ('header','request','asset','description',)
		return form
	"""
	

	
	
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			if getattr(obj, 'header', None) == None:
				readonly_fields = ('asset','request','descriptionx',)
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
				readonly_fields += ('asset','request','descriptionx',)
				
		elif data.name == 'unit':
			if getattr(obj, 'header', None) != None:
				readonly_fields = ('header','asset','request','descriptionx',)
			else :
				readonly_fields = ('header',)
				
			xx = False
			try:
				x = getattr(obj,'header',None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == True:
				readonly_fields += ('header','asset','request','descriptionx',)
			else :
				readonly_fields +=()
		
		return readonly_fields
		
		"""
		if data.name == 'staff':
				xx = False
				try:
					x = getattr(obj,'header',None)
					xx = x.department_staff_aggrement
				except: pass
				if xx == False:
					readonly_fields = ('asset','request','description',)
				else: 
					readonly_fields = ('header','asset','request','description',)
				
		elif data.name == 'unit':
			readonly_fields = ('header','request','asset','description',)
		else:
			readonly_fields = ()
		return readonly_fields
	"""
	"""
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			if getattr(obj, 'header', None) != None:
				readonly_fields = ('header',)
			else :
				readonly_fields = ('asset','request','description',)
		else: 
			readonly_fields = ('header','asset','request','description',)
		
		return readonly_fields
	"""
	
admin.site.register(Data_disposal_request, Data_disposal_request_admin)
