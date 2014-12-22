from django.contrib import admin
from Apps.Asset.Request.models import *
from django.forms.models import BaseInlineFormSet
from django.contrib.auth.models import Group
from Apps.Distribution.master_sales.models import *

#class Choice_service_admin(admin.ModelAdmin):
#	list_display = ['service']
#	search_fields = ['service']
	
#admin.site.register(Choice_service, Choice_service_admin)

class DataUserRequestInline(admin.StackedInline):
	model = Data_user_request
	extra = 0
	verbose_name = "Data Request"
	readonly_fields = ('header','asset','choice_service','date_used','answer_service','description','asset_reply',)
	
class Header_user_request_admin(admin.ModelAdmin):
	list_display = ['no_reg','user','req_date','department_staff_aggreement']
	search_fields = ['no_reg','department']
	inlines = [DataUserRequestInline,]
	date_hierarchy = 'req_date'
	
	def suit_row_attributes(self, obj, request):
		css_class = {
			True:'success', False: 'error',}.get(obj.department_staff_aggreement)
		if css_class:
			return {'class': css_class, 'data': obj.department_staff_aggreement}
	
	def save_model(self, request, Header_user_request,form,change):
		dep = Group.objects.get(user=request.user)
		dep2 = StaffPerson.objects.get(user=request.user)
		if dep.name == 'unit':
			Header_user_request.department = dep2.employee.department
		Header_user_request.save()
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		data2 = StaffPerson.objects.get(user=request.user)
		form = super(Header_user_request_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'unit':
			try:
				x = getattr(obj,'department_staff_aggreement', False)
			except: pass
			if x == False:
				form.base_fields['user'].queryset = form.base_fields['user'].queryset.filter(department=data2.employee.department)
			else : 
				readonly_fields = ('user',)
		else: 
			readonly_fields = ('no_reg','user','req_date','department_staff_aggreement',)
		return form

	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		data = Ms_asset.objects.filter(usage_status = 1)
		if user.name=='unit':
			return Header_user_request.objects.filter(department=user2.employee.department)
		else :
			return Header_user_request.objects.all()	
			
		if request.user.is_superuser:
			return Header_user_request.objects.all()
	
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			readonly_fields = ('department',)
			if getattr(obj, 'department_staff_aggreement', None) == True:
				readonly_fields = ('user','department','department_staff_aggreement',) 	
			
				
		elif data.name == 'staff':
			readonly_fields += ('no_reg','user','department','department_staff_aggreement',)
		
		if request.user.is_superuser:
			readonly_fields = ()
		return readonly_fields
	
admin.site.register(Header_user_request, Header_user_request_admin)

class Data_user_request_admin(admin.ModelAdmin):
	list_display = ['ID','header','date_used', 'choice_service','answer_service']
	save_on_top = True
	ordering = ('-asset', )
	list_filter = ['choice_service',]
	
	def suit_row_attributes(self, obj, request):
		css_class = {
			11:'success',2:'success',13:'success',4:'success',5:'success',6:'success',7:'error'}.get(obj.answer_service)
		if css_class:
			return {'class': css_class, 'data': obj.answer_service}
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		data2 = StaffPerson.objects.get(user=request.user)
		form = super(Data_user_request_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'unit':
			xx = False
			try:
				x = getattr(obj, 'header', None)
				xx = x.department_staff_aggreement
			except: pass
			if xx == False:
				form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=data2.employee.department)
				form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(usage_status=1)
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggreement=False)
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department=data2.employee.department)
				self.exclude = ['asset_reply']
			else :
				self.exclude = ['asset_reply','description',]
		else : 
			xx = False
			try:
				x = getattr(obj, 'header', None)
				xx = x.department_staff_aggreement
			except: pass
			if xx == False:
				self.exclude = ['description',] 
			else: self.exclude = ['asset_reply','description',] 
		return form
		
			
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			xx = False
			try:
				x = getattr(obj, 'header', None)
				xx = x.department_staff_aggreement
			except: pass
			if xx == False:
				readonly_fields = ('answer_service','asset_replyx',)
			else: 
				readonly_fields = ('header','asset','choice_service','date_used','answer_service','descriptionx','asset_replyx',)
			
		elif data.name == 'staff':
			xx = False
			try:
				x = getattr(obj, 'header', None)
				xx = x.department_staff_aggreement
			except: pass
			if xx == False:
				readonly_fields += ('header','choice_service','descriptionx','asset','date_used',)
			else: 
				readonly_fields += ('header','choice_service','descriptionx','asset','date_used','answer_service','asset_replyx',)
				
		if request.user.is_superuser:
			readonly_fields = ()
		return readonly_fields
	"""		
			if getattr(obj, 'header', None) != None:
				readonly_fields += ('header','choice_service','description','asset','date_used',)
		"""	
		
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		data = Ms_asset.objects.filter(usage_status = 1)
		if user.name=='unit':
			return Data_user_request.objects.filter(header__department=user2.employee.department)
		elif user.name=='staff' :
			return Data_user_request.objects.all()	
		elif request.user.is_superuser:
			return Data_user_request.objects.all()
	
admin.site.register(Data_user_request, Data_user_request_admin)

