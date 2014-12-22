from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.const import *
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import Department
from Apps.Asset.Request.models import *
from datetime import datetime
from tinymce.models import HTMLField
from Apps.Distribution.master_sales.models import *


class Disposal_status(models.Model):
	disposal_status = models.IntegerField(verbose_name=_('Status Penghapusan  '), choices=Status_penghapusan)
	description = models.TextField(verbose_name=_('Description '), blank=True)

	class Meta:
		verbose_name_plural="Status Penghapusan"
		verbose_name="Status_Penghapusan"
		
	def __unicode__(self):
		return '%s' % self.id

class Header_disposal_request(models.Model):
	no_reg = models.CharField(verbose_name='No. Reg Penghapusan', max_length=25, editable=False)
	department = models.ForeignKey(Department, verbose_name=_('Nama Departement '))
	disposal_date = models.DateTimeField(verbose_name=_('Tanggal '), auto_now_add=True)
	asset_staff_review = HTMLField(verbose_name=_('Asset Staff Detail '), blank=True)
	department_staff_review = HTMLField(verbose_name=_('Department Staff Review '), blank=True)
	department_staff_aggrement = models.BooleanField(verbose_name=_('Persetujuan Department Staff'), default=False ,help_text=')* Jangan Disetujui Dulu Sebelum Data Penghapusan Dimasukkan')
	disposal_status = models.BooleanField(verbose_name=_('Status Penghapusan '),default=False, help_text=')* Centang Setelah ada Persetujuan dari Department')
	
	class Meta:
		verbose_name_plural="Header Disposal Request"
		verbose_name="Header_Disposal_Request"
	
	def asset_reviewx(self):
		return '%s' % self.asset_staff_review
	asset_reviewx.allow_tags = True
	asset_reviewx.short_description = 'Asset Staff Review'
	
	def dept_reviewx(self):
		return '%s' % self.department_staff_review
	dept_reviewx.allow_tags = True
	dept_reviewx.short_description = 'Deskripsi'
	
		
	def incstring(self):
		try:
			data = Header_disposal_request.objects.all()
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
		return 'PH/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
	
	def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
		if self.no_reg =='':
			self.no_reg = self.no_rek()
		else:
			self.no_reg = self.no_reg
		super(Header_disposal_request, self).save()
		
	def __unicode__(self):
		return u'%s' % self.no_reg

class Data_disposal_request(models.Model):
	header = models.ForeignKey(Header_disposal_request, verbose_name=_('Header Disposal Request  '))
	request = models.OneToOneField(Data_user_request, verbose_name=_('No. Permintaan '), blank=True, null=True)
	asset = models.ForeignKey(Ms_asset, verbose_name=_('Nama Asset '), blank=True, null=True)
	
	description = HTMLField(verbose_name=_('Deskripsi '), blank=True, null=True)
	
	class Meta:
		verbose_name_plural="Data Disposal Request"
		verbose_name="Data_Disposal_Request"
	
	def descriptionx(self):
		return '%s' % self.description
	descriptionx.allow_tags = True
	descriptionx.short_description = 'Deskripsi'
	
	def __unicode__(self):
		return u'%s' % self.id

#def create_user_profile(sender, instance, created, **kwargs):  
#	if created == True:  
#		profile, created = Role_user.objects.get_or_create(user=instance)
        
#post_save.connect(create_user_profile, sender=User)


def disposal(sender, instance, created, **kwargs):  
	if instance.disposal_status == True:  
		data = {}
		data = Data_disposal_request.objects.filter(header=instance)
		for d in data:
			aset = Ms_asset.objects.get(no_reg=d.asset.no_reg)
			try:
				ha = Historical_asset.objects.get(no_reg=aset.no_reg)
			except:
				backup = Historical_asset(no_reg=aset.no_reg, asset_name=aset.asset_name, type=aset.type, department=aset.department, add_date=aset.add_date)
				backup.save()	
				
				x = Ms_asset.objects.get(id=d.asset.id)
				stat = Ms_asset(id=x.id, no_reg=x.no_reg, asset_name=x.asset_name, type=x.type, end_warranty=x.end_warranty, location=x.location,department=x.department, price=x.price, life_time=x.life_time, salvage=x.salvage, condition=x.condition, add_date=x.add_date, freq_m=x.freq_m, status_loan=x.status_loan, usage_status=2)
				stat.save()
			
post_save.connect(disposal, sender=Header_disposal_request)










