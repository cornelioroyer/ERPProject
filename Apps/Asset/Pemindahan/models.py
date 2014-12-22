from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import Department
from Apps.Asset.Master.models import *
from Apps.Asset.Request.models import *
from datetime import datetime
from tinymce.models import HTMLField

class Moving_status(models.Model):
	asset_moving = models.CharField(verbose_name=_('Status Pemindahan '), max_length=20)
	description = HTMLField(verbose_name=_('Deskripsi '), blank=True)

	class Meta:
		verbose_name_plural="Status Pemindahan"
		verbose_name="Status_Pemindahan"
		
	def __unicode__(self):
		return '%s' % self.asset_moving


class Header_moving_request(models.Model):
	no_reg = models.CharField(verbose_name='No. Reg Pemindahan ', max_length=25, editable=False)
	from_department = models.ForeignKey(Department, related_name=_('Department Asal Asset'), help_text='Department Pemilik' )
	to_department = models.ForeignKey(Department, related_name=_('Department yang Dituju '),help_text='Department Penerima')
	moving_add_date = models.DateField(verbose_name=_('Tanggal '), auto_now_add=True)
	asset_staff_review = HTMLField(verbose_name=_('Asset Staff Review '), blank=True)
	department_staff_review = HTMLField(verbose_name=_('Department Staff Review '), blank=True)
	department_staff_aggrement = models.BooleanField(verbose_name=_('Persetujuan Department Staff'),default=False, help_text=')* Jangan Disetujui dulu Sebelum Data Pemindahan Asset Dimasukkan')
#	asset_staff_agrement = models.BooleanField(verbose_name=_('Persetujuan Asset Staff'))
	
	class Meta:
		verbose_name_plural="Header Moving Request"
		verbose_name="Header_Moving_Request"
		
	def asset_reviewx(self):
		return '%s' % self.asset_staff_review
	asset_reviewx.allow_tags = True
	asset_reviewx.short_description = 'Asset Staff Review'
	
	def dept_reviewx(self):
		return '%s' % self.department_staff_review
	dept_reviewx.allow_tags = True
	dept_reviewx.short_description = 'Department Staff Review'
	
	def incstring(self):
		try:
			data = Header_moving_request.objects.all()
			jml = data.count()
		except:
			jml=0
		pass
		no = 0
		if jml == 0:
			no = 0
		else:
			for d in data:
				split = str(d.no_reg).split('/')
				no = int(split[3])
		num = no + 1
		cstring = str(num)
		return cstring
	
	def inclen(self):
		leng = len(self.incstring())
		return leng
	
	def no_rek(self):
		date = datetime.now()
		now = date.strftime("%m")
		nowyear = date.strftime("%Y")
		intnow = int(now)
		intyear = int(nowyear)
		strnow = str(intnow)
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		nol = 5 - self.inclen()
		if nol == 1: num = "0"
		elif nol == 2: num = "00"
		elif nol == 3: num = "000"
		elif nol == 4: num = "0000"
		number = num + self.incstring()
		return 'PD/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
	
	def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
		if self.no_reg =='':
			self.no_reg = self.no_rek()
		else:
			self.no_reg = self.no_reg
		super(Header_moving_request, self).save()
		
	def __unicode__(self):
		return '%s' % self.no_reg
	
			
class Data_moving_request(models.Model):
	header = models.ForeignKey(Header_moving_request, verbose_name=_('Header Moving Request  '))
	request = models.OneToOneField(Data_user_request, verbose_name=_('No.Permintaan '), blank=True, null=True)
	asset = models.ForeignKey(Ms_asset, verbose_name=_('Nama Asset '), blank=True, null=True)
	moving_status = models.ForeignKey(Moving_status, verbose_name=_('Status Pemindahan '), blank=True, null=True)
	description = models.TextField(verbose_name=_('Deskripsi '), blank=True, null=True)
#	quantity = models.IntegerField(verbose_name=_('Jumlah '), max_length=10)
	
	
	class Meta:
		verbose_name_plural="Data Moving Request"
		verbose_name="Data_Moving_Request"
		
	def __unicode__(self):
		return '%s' % self.id
	
	
#	def save(self, force_insert=False, force_update=False, using=None):
#		data = Ms_asset.objects.update(department=self.header.to_department)
#		super(Data_moving_request, self).save()

def moving(sender, instance, created, **kwargs):
	if instance.department_staff_aggrement == True:  
		data = Data_moving_request.objects.filter(header=instance)
		for d in data:				
			aset = Ms_asset.objects.get(id=d.asset.id)
			move = Ms_asset(id=aset.id, no_reg=aset.no_reg, asset_name=aset.asset_name, type=aset.type, end_warranty=aset.end_warranty, location=aset.location,department=instance.to_department, price=aset.price, life_time=aset.life_time, salvage=aset.salvage, condition=aset.condition, add_date=aset.add_date, freq_m=aset.freq_m, status_loan=aset.status_loan)
			move.save()	
						
post_save.connect(moving, sender=Header_moving_request)	
