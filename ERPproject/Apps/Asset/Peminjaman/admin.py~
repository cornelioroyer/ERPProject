from django.contrib import admin
from Apps.Asset.Peminjaman.models import *
from django.contrib.auth.models import Group
from Apps.Distribution.master_sales.models import *

class DataLoaningInline(admin.TabularInline):
	model = Data_loaning_request
	extra = 1
	max_num = 0
	can_delete = True
	readonly_fields = ('header','request','asset','description')

class Header_loaning_request_admin(admin.ModelAdmin):
	list_display = ['no_reg','start_loan_date','end_loan_date','from_department','to_department','department_staff_aggrement']
	search_fields = ['no_reg']
	inlines = [DataLoaningInline,]
	list_filter = ['start_loan_date','department_staff_aggrement',]
		
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			readonly_fields += ('no_reg','from_department','to_department','start_loan_date','end_loan_date',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields += ('department_staff_aggrement','department_staff_review')
		
		elif data.name == 'staff':
			readonly_fields += ('department_staff_review','department_staff_aggrement',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields += ('from_department','to_department','start_loan_date','end_loan_date',)
		#	else:
		#		readonly_fields += ('status',)
		#		if getattr(obj, 'status', None) == True:
		#			readonly_fields += ('no_reg','start_loan_date','end_loan_date','from_department','to_department',)
			
		return readonly_fields
		
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		data = Ms_asset.objects.filter(usage_status = 1)
		if user.name=='unit':
			return Header_loaning_request.objects.filter(from_department=user2.employee.department)
		else :
			return Header_loaning_request.objects.all()	
			
		if request.user.is_superuser:
			return Header_loaning_request.objects.all()
	
admin.site.register(Header_loaning_request, Header_loaning_request_admin)

class Data_loaning_request_admin(admin.ModelAdmin):
	list_display = ['header','request','asset','descriptionx']
	search_fields = ['header','asset']
	list_filter = ['request','asset']
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		if user.name=='unit':
			return Data_loaning_request.objects.filter(header__from_department=user2.employee.department)
		else :
			return Data_loaning_request.objects.all()	
			
		if request.user.is_superuser:
			return Data_loaning_request.objects.all()	
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Data_loaning_request_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			x = getattr(obj, 'header', None)
			xx = True
			if getattr(obj, 'header', None) == None:
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
				self.exclude = ['description',]
			else :						
				if getattr(obj, 'header', None) != None:
					if x.department_staff_aggrement == False:
						form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.from_department,usage_status=1)
						form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service=5)
										
					else:
						self.exclude = ['description',]
					
		else:
			readonly_fields = ('header','request','asset','description',)
			self.exclude = ['description',]	
				
		return form
		
	
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
				readonly_fields += ('descriptionx','asset','request',)
				
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
			if xx == False:
				readonly_fields += ('header','request','asset','descriptionx',)
			else :
				readonly_fields +=()
				
		return readonly_fields	
	
	
admin.site.register(Data_loaning_request, Data_loaning_request_admin)

class Header_return_request_admin(admin.ModelAdmin):
	list_display = ['header','return_date','review','department_staff_aggrement']
	search_fields = ['header','return_date']
	list_filter = ['return_date','department_staff_aggrement',]
	
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Header_return_request_admin, self).get_form(request, obj, **kwargs)
		
		if data.name == 'staff':
			xx = False
			try:
				x = getattr(obj,'header', None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == False:
				#form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.from_department)
				#form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(usage_status=1)
				#form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service=5)
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=True)
			else :
				self.exclude = ['asset_staff_review',] 
		else:
			readonly_fields = ('header','return_date','review','department_staff_aggrement',)
		return form
				
	"""
		if data.name == 'staff':
			x = getattr(obj, 'header', None)
			if getattr(obj, 'header', None) != None:
				form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service=5)
				form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.from_department)
			else:
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=True)
		return form
		"""
		
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			readonly_fields += ('header','review',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields += ('department_staff_aggrement',)
		
		elif data.name == 'staff':
			readonly_fields += ('department_staff_aggrement',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields += ('header','return_date','review',)
		#	else:
		#		readonly_fields += ('status',)
		#		if getattr(obj, 'status', None) == True:
		#			readonly_fields += ('no_reg','start_loan_date','end_loan_date','from_department','to_department',)
			
		return readonly_fields
	
	"""
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			readonly_fields = ('department_staff_aggrement',)
		else: 
			readonly_fields = ('header','return_date','asset_staff_review',)
		
		return readonly_fields	
	"""
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		if user.name=='unit':
			return Header_return_request.objects.filter(header__from_department=user2.employee.department)
		else :
			return Header_return_request.objects.all()	
			
		if request.user.is_superuser:
			return Header_return_request.objects.all()	
		
admin.site.register(Header_return_request, Header_return_request_admin)

#class Data_return_request_admin(admin.ModelAdmin):
#	list_display = ['header','loaning','status']
#	search_fields = ['header','loaning','status']
	
#admin.site.register(Data_return_request, Data_return_request_admin)
