from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.const import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import signals
from tinymce.models import HTMLField
from Apps.Hrm.Master_General.models import Department, Section

class Loaning_status(models.Model):
	loaning_status = models.CharField(verbose_name=_('Status Peminjaman  '), max_length=30)
	description = HTMLField(verbose_name=_('Description '), blank=True)

	class Meta:
		verbose_name_plural="Status Peminjaman"
		verbose_name="Status_Peminjaman"
		
	def __unicode__(self):
		return '%s' % self.loaning_status

class Location(models.Model):
	location_name = models.CharField(verbose_name=_('Lokasi  '), max_length=30)
	
	class Meta:
		verbose_name_plural="Lokasi"
		verbose_name="Lokasi"
		
	def __unicode__(self):
		return '%s' % self.location_name	
"""
class Maintenance_status(models.Model):
	maintenance_status = models.IntegerField(verbose_name=_('Status Maintenance '), choices=status_maintenace)
	
	class Meta:
		verbose_name_plural="Status Pemeliharaan"
		verbose_name="Status_Pemeliharaan"
		
	def __unicode__(self):
		return '%s' % self.maintenance_status
"""
class Asset_type(models.Model):
	type = models.CharField(verbose_name=_('Type  '), max_length=35)
	
	class Meta:
		verbose_name_plural="Asset Type"
		verbose_name="Asset Type"
		
	def __unicode__(self):
		return '%s' % self.type

class Asset_currency(models.Model):
	currency_symbol = models.CharField(verbose_name='Simbol', max_length=5)
	currency_name = models.CharField(verbose_name='Mata Uang', max_length=20)
	currency_rate = models.DecimalField(verbose_name='Nilai Tukar', decimal_places=2, max_digits=10, default=1)
	
	class Meta:
		verbose_name = 'Mata Uang'
		verbose_name_plural = 'Mata Uang'
		ordering = ['id']
	
	def __unicode__(self):
		return '%s' % self.currency_symbol
"""		
class Department(models.Model):
	department_name = models.CharField(verbose_name=_('Nama Departemen'),max_length=40 )
	description = HTMLField(verbose_name=_('Deskripsi '), blank=True)
	
	class Meta:
		verbose_name_plural = 'Departemen'
		verbose_name = 'Departemen'
		
	def __unicode__(self):
		return '%s' % self.department_name
"""			
class Code_unit(models.Model):
	unit_name = models.CharField(verbose_name=_('Nama Unit '),max_length=40 )
	
	class Meta:
		verbose_name_plural = 'Nama Unit'
		verbose_name = 'Nama_Unit'
		
	def __unicode__(self):
		return '%s' % self.unit_name			

"""		
class Section(models.Model):	
	section_name = models.CharField(verbose_name=_('Nama Seksi'),max_length=100 )
	
	class Meta:
		verbose_name_plural = 'Seksi'
		verbose_name = 'Seksi'
		
	def __unicode__(self):
		return '%s' % self.section_name
"""
"""
class Employee(models.Model):
	NIP = models.IntegerField(verbose_name=_('NIP '),max_length=50 )
	employee_name = models.CharField(verbose_name=_('Nama Pegawai '),max_length=70 )
	birthday = models.DateField(verbose_name=_('Tanggal Lahir '))
	unit = models.ForeignKey(Code_unit, verbose_name=_('Nama Unit '))
	department = models.ForeignKey(Department, verbose_name=_('Nama Departemen '))
	section = models.ForeignKey(Section, verbose_name=_('Nama Seksi '))
	address = models.CharField(verbose_name=_('Alamat '),max_length=70 )
	city = models.CharField(verbose_name=_('Kota Asal '),max_length=70 )
	NPWP = models.IntegerField(verbose_name=_('NPWP	 '),max_length=50 )
	
	class Meta:
		verbose_name_plural = 'Karyawan'
		verbose_name = 'Karyawan'
		
	def __unicode__(self):
		return '%s' % self.employee_name
"""
class Vendor(models.Model):	
	vendor_name = models.CharField(verbose_name=_('Nama Vendor '),max_length=50 )
	vendor_type = models.IntegerField(verbose_name=_('Type Vendor '),choices=Tipe_vendor )
	Description = HTMLField(verbose_name=_('Deskripsi '),max_length=50 )

	class Meta:
		verbose_name_plural = 'Vendor'
		verbose_name = 'Vendor'
	def __unicode__(self):
		return '%s' % self.vendor_name

class Unit_of_measure_asset(models.Model):	
	unit_of_measure_detail = models.CharField(verbose_name=_('Nama Satuan '),max_length=50 )
	
	class Meta:
		verbose_name_plural = 'Satuan'
		verbose_name = 'Satuan'
		
	def __unicode__(self):
		return '%s' % self.unit_of_measure_detail	

class Ms_customer(models.Model):	
	username = models.CharField(verbose_name=_('Username'),max_length=50 )
	password = models.CharField(verbose_name=_('Password '),max_length=10 )
	customer_name = models.CharField(verbose_name=_('Nama Pembeli'),max_length=50 )
	customer_address = models.CharField(verbose_name=_('Alamat '),max_length=50 )
	customer_city = models.CharField(verbose_name=_('Kota '),max_length=50 )
	customer_phone = models.CharField(verbose_name=_('No. Telp '),max_length=50 )
	fax = models.CharField(verbose_name=_('fax'),max_length=50 )
	email = models.CharField(verbose_name=_('E-mail'),max_length=50 )
	customer_verified = models.BooleanField(verbose_name=_('Verifikasi Customer'),default=False)
	
	class Meta:
		verbose_name_plural = 'Customer'
		verbose_name = 'Customer'
		
	def __unicode__(self):
		return '%s' % self.username	

class Role_user_asset(models.Model):
	user = models.OneToOneField(User)
	access_level = models.CharField(max_length=30, choices=LEVEL_AKSES_CHOICES, verbose_name='Level Akses')
	intern_occupation = models.CharField(max_length=30, blank=True, null=True)
	intern_date_register = models.DateField(auto_now_add=True)
	department = models.ForeignKey(Department, blank=True, null=True)
	
	class Meta:
		verbose_name = 'Hak Akses Asset'
		verbose_name_plural = 'Hak Akses Asset'
		ordering = ['id']
	
	def __unicode__(self):
		return "%s" % self.user

def create_user_profile(sender, instance, created, **kwargs):  
	if created == True:  
		profile, created = Role_user_asset.objects.get_or_create(user=instance)
        
post_save.connect(create_user_profile, sender=User)


