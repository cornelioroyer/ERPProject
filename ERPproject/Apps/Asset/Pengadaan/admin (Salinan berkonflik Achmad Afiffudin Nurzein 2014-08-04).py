from django.contrib import admin
from Apps.Asset.Pengadaan.models import *
from django.contrib.auth.models import Group

class DataRequestInline(admin.StackedInline):
	model = Data_request_asset
	extra = 0
	max_num = 1
	can_delete = True
	readonly_fields =('header_request','request','ra_amount','ra_used','unit_of_measure','description',)
	
	
	#readonly_fields = ('header_request','request','ra_amount','ra_used','unit_of_measure','description')
	"""def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			if getattr(obj, 'ra_lock', None) == True:
				readonly_fields = ('header_request','request','ra_amount','unit_of_measure','ra_used','description',)
			else :
				readonly_fields = ('header_request','request','ra_amount','unit_of_measure','ra_used','description',)
		else: 
			readonly_fields = ()
		
		return readonly_fields	
	"""	
class Header_request_asset_admin(admin.ModelAdmin):
	list_display = ['no_reg','department','ra_add_date','ra_lock_date','ra_lock']
	search_fields = ['no_reg','department','ra_lock']
	inlines = [DataRequestInline,]
	list_filter = ['ra_add_date','ra_lock','department',]
		
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			readonly_fields += ('no_reg','department','ra_lock_date','asset_staff_review',)
			if getattr(obj, 'ra_lock', None) == True:
				readonly_fields += ('ra_lock',)
		elif data.name == 'staff':
			readonly_fields = ()
			if getattr(obj, 'ra_lock', None) == True:
				readonly_fields +=('no_reg','department','ra_lock_date','asset_staff_review','ra_lock',)
			else : 
				readonly_fields =('ra_lock',)			
		return readonly_fields	
		
		
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		if user.name=='unit':
			return Header_request_asset.objects.filter(department=user.department)
		else :
			return Header_request_asset.objects.all()	
			
		if request.user.is_superuser:
			return Header_request_asset.objects.all()
			
admin.site.register(Header_request_asset, Header_request_asset_admin)

class Data_request_asset_admin(admin.ModelAdmin):
	list_display = ['header_request','request','ra_amount','ra_used','unit_of_measure','descriptionx']
	search_fields = ['no_item','header_request']
	list_filter = ['request',]
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		if user.name=='unit':
			return Data_request_asset.objects.filter(header_request__department=user.department)
		else :
			return Data_request_asset.objects.all()	
			
		if request.user.is_superuser:
			return Data_request_asset.objects.all()
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Data_request_asset_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			xx = False
			try:
				x = getattr(obj,'header_request', None)
				xx = x.ra_lock
			except: pass
			if xx == False:
				form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service__startswith = 1)#jaga2 untuk permintaan penggantian
				form.base_fields['header_request'].queryset = form.base_fields['header_request'].queryset.filter(ra_lock=False)
			else :
				self.exclude = ['description',] 
		if data.name == 'unit':
			self.exclude = ['description',] 
		return form
		
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
				xx = False
				try:
					x = getattr(obj,'header_request',None)
					xx = x.ra_lock
				except: pass
				if xx == True:
					readonly_fields += ('header_request','ra_amount','request','ra_used','descriptionx','unit_of_measure',)
				else: 
					readonly_fields = ()
				
		elif data.name == 'unit':
				xx = False
				try:
					x = getattr(obj,'header_request',None)
					xx = x.ra_lock
				except: pass
				if xx == True:
					readonly_fields += ('header_request','request','ra_amount','ra_used','descriptionx','unit_of_measure',)
				else: 
					readonly_fields = ('header_request','request','ra_amount','ra_used','descriptionx','unit_of_measure',)
		
		return readonly_fields	
	

admin.site.register(Data_request_asset, Data_request_asset_admin)


