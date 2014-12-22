from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from Apps.Asset.Property_asset.models import *
from Apps.Asset.Penjualan.models import *
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget

class Register(UserCreationForm):
	password = forms.PasswordInput()
	class Meta:
		model = Ms_customer
		exclude = ('customer_verified','password')
	
	def save(self, commit=True):
		if commit:
			c = super(UserCreationForm, self).save(commit=True)
			c.password = self.cleaned_data["password1"]
			c.save()
		return c

class Proc_register(ModelForm):
	class Meta:
		model = Customer_proc
		exclude = ('customer', 'procurement')

class EditData(ModelForm):
	class Meta:
		model = Ms_customer
		exclude = ('username','password','customer_verified')
	

#class Post_bidding(ModelForm):
#	class Meta:
#		model = Bidding
#		exclude = ('custom_proc', 'uname')
#	def save (self, comit=True):
#		x = super(UserCreationForm, self).save(comit=True)
#		x.save()
#	return x
		
"""
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
"""
