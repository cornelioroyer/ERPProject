from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from Apps.Procurement.vendor.models import *
from Apps.Procurement.internal.models import *
from Apps.Procurement.publicTender.models import *
from django.forms import ModelForm
from django.contrib.admin import widgets
from tinymce.models import HTMLField
from django.forms.extras.widgets import SelectDateWidget

class Register(UserCreationForm):
	"""my form"""
	password = forms.PasswordInput()
	
	
	class Meta:
		model = Ms_Vendor
		exclude = ('vendor_verified','date_register','password')
	
	def save(self, commit=True):
		if commit:
			vendor = super(UserCreationForm, self).save(commit=True)
			vendor.password = self.cleaned_data["password1"]
			vendor.save()
		return vendor

class EditData(ModelForm):
	class Meta:
		model = Ms_Vendor
		exclude = ('password','date_register','vendor_verified')

class Siup(ModelForm):
	
	class Meta:
		model = Siup_Vendor
		widgets = {
                'ms_vendor_id': forms.HiddenInput(),
            }
	
	def __init__(self, *args, **kwargs):
		super(Siup, self).__init__(*args, **kwargs)
		self.fields['siup_valid_until'].widget = SelectDateWidget()

class Iujk(ModelForm):
	
	class Meta:
		model = Iujk_Vendor
		widgets = {
                'ms_vendor_id': forms.HiddenInput(),
            }
	
	def __init__(self, *args, **kwargs):
		super(Iujk, self).__init__(*args, **kwargs)
		self.fields['iujk_valid_until'].widget = SelectDateWidget()

class Apbu(ModelForm):
	
	class Meta:
		model = Apbu_Vendor
		widgets = {
                'ms_vendor_id': forms.HiddenInput(),
            }
	
	def __init__(self, *args, **kwargs):
		super(Apbu, self).__init__(*args, **kwargs)
		self.fields['apbu_valid_until'].widget = SelectDateWidget()

class Klasifikasi(ModelForm):
	class Meta:
		model = Classification_Vendor
		widgets = {
                'ms_vendor_id': forms.HiddenInput(),
            }

class Doc_Vendor(ModelForm):
	class Meta:
		model = Documents_Vendor
		widgets = {
                'ms_vendor_id': forms.HiddenInput(),
            }
			
class Owner(ModelForm):
	class Meta:
		model = Owner_Vendor
		widgets = {
                'ms_vendor_id': forms.HiddenInput(),
            }

class Direksi(ModelForm):
	class Meta:
		model = Board_Of_Directors_Vendor
		widgets = {
                'ms_vendor_id': forms.HiddenInput(),
            }

class TenagaAhli(ModelForm):
	class Meta:
		model = Experts_Vendor
		widgets = {
                'ms_vendor_id': forms.HiddenInput(),
            }
	
	def __init__(self, *args, **kwargs):
		super(TenagaAhli, self).__init__(*args, **kwargs)
		self.fields['ska_valid_until'].widget = SelectDateWidget()

class DataPlan(ModelForm):
	class Meta:
		model = Data_Plan
		exclude = ('plan_total_rupiah', 'plan_total_price')
		widgets = {
			'header_plan_id': forms.HiddenInput(),
			}
	
	def __init__(self, *args, **kwargs):
		super(DataPlan, self).__init__(*args, **kwargs)
		self.fields['plan_used'].widget = SelectDateWidget()

class DataReq(ModelForm):
	class Meta:
		model = Data_Purchase_Request
		exclude = ('request_total_rupiah', 'request_total_price','method_choices','no_po','state_choices')
		widgets = {
			'header_purchase_request_id': forms.HiddenInput(),
			}
	
	def __init__(self, *args, **kwargs):
		super(DataReq, self).__init__(*args, **kwargs)
		self.fields['request_used'].widget = SelectDateWidget()

class VendorProc(ModelForm):
	class Meta:
		model = Vendor_Proc
		exclude = ('ms_vendor', 'announcement_proc')

class DataRo(ModelForm):
	class Meta:
		model = Data_Rush_Order
		exclude = ('ro_total_rupiah', 'ro_total_price','method_choices','no_po','state_choices')
		widgets = {
			'header_rush_order_id': forms.HiddenInput(),
			}
	
	def __init__(self, *args, **kwargs):
		super(DataRo, self).__init__(*args, **kwargs)
		self.fields['ro_used'].widget = SelectDateWidget()

class Login(UserCreationForm):
	username = forms.CharField(max_length=254)
	password = forms.PasswordInput()