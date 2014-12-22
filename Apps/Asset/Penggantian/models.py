from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import *
from Apps.Asset.Master.models import *
from Apps.Asset.Request.models import *
from datetime import datetime
from tinymce.models import HTMLField


class Header_change_request(models.Model):
	no_reg = models.CharField(verbose_name='No. Reg Penggantian', max_length=25, editable=False)
	department = models.ForeignKey(Department, verbose_name=_('Nama Department '))
	change_date = models.DateField(verbose_name=_('Tanggal '), auto_now_add=True)
	asset_staff_review = models.TextField(verbose_name=_('Asset Staff Review '), blank=True)
	department_staff_review = models.TextField(verbose_name=_('Department Staff Review '), blank=True)
	department_staff_aggrement = models.BooleanField(verbose_name=_('Persetujuan Department Staff'),default=False ,help_text=')*Jangan Di Setujui dahulu sebelum Data Penggantian dimasukkan')
	
		
	class Meta:
		verbose_name_plural="Header Change Request"
		verbose_name="Header_Change_Request"
	
	def incstring(self):
		try:
			data = Header_change_request.objects.all()
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
		return 'PG/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
	
	def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
		if self.no_reg =='':
			self.no_reg = self.no_rek()
		else:
			self.no_reg = self.no_reg
		super(Header_change_request, self).save()
		
	def __unicode__(self):
		return '%s' % self.no_reg


class Data_change_request(models.Model):
	header = models.ForeignKey(Header_change_request, verbose_name=_('Header Change Request  '))
	request = models.OneToOneField(Data_user_request, verbose_name=_('No. Permintaan '), blank=True, null=True, help_text='Hanya untuk satu permintaan')
	asset = models.ForeignKey(Ms_asset, verbose_name=_('Nama Asset '), blank=True, null=True)
	change_status = models.IntegerField(verbose_name=_('Status Penggantian '),choices=status_ganti, default=2)
	description = HTMLField(verbose_name=_('Deskripsi '), blank=True, null=True)
	
	class Meta:
		verbose_name_plural="Data Change Request"
		verbose_name="Data_Change_Request"
	
	def descriptionx(self):
		return '%s' % self.description
	descriptionx.allow_tags = True
	descriptionx.short_description = 'Deskripsi'
	
	def __unicode__(self):
		return '%s' % self.id


def change(sender, instance, created, **kwargs):  
	if instance.department_staff_aggrement == True:  
		data = Data_change_request.objects.filter(header=instance)
		for d in data:
			aset = Ms_asset.objects.get(id=d.asset.id)
			try:
				ha = Historical_asset.objects.get(no_reg=aset.no_reg)
			except :	
				backup = Historical_asset(no_reg=aset.no_reg, asset_name=aset.asset_name, type=aset.type, department=aset.department, add_date=aset.add_date)
			
				backup.save()	
			
			#Ms_asset.objects.filter(id=d.asset.id).delete()
			x = Ms_asset.objects.get(id=d.asset.id)
			stat = Ms_asset(id=x.id, no_reg=x.no_reg, asset_name=x.asset_name, type=x.type, end_warranty=x.end_warranty, location=x.location,department=x.department, price=x.price, life_time=x.life_time, salvage=x.salvage, condition=x.condition, add_date=x.add_date, freq_m=x.freq_m, status_loan=x.status_loan, usage_status=2)
			stat.save()
post_save.connect(change, sender=Header_change_request)
		
class Data_request_asset_change(models.Model):
	header_asset = models.ForeignKey(Header_change_request, verbose_name=_('Data Change Request  '))
	title = models.CharField(verbose_name=_('Nama Permintaan '), max_length=50)
	detail = HTMLField(verbose_name=_('Detail Permintaan '), blank=True, help_text='Isi Kriteria Permintaan Penggantian ')
	ra_used = models.DateField(verbose_name=_('Waktu Penggunaan '), blank=True, null=True)
	ra_amount = models.IntegerField(verbose_name=_('Jumlah '), blank=True, null=True)
	send_request = models.BooleanField(verbose_name=_('Dikirim ?'), default=False)
	
	class Meta:
		verbose_name_plural="Request Asset from Change"
		verbose_name="request_asset_from_Change"
		
	def detailx(self):
		return '%s' % self.detail
	detailx.allow_tags = True
	detailx.short_description = 'Deskripsi'
	
	
	def __unicode__(self):
		return  '%s' % self.header_asset
		
#	def desc(self):
#		des = Data_user_request.objects.get(id=self.request.id)
#		return des.description
#	desc.short_description='Deskripsi'	
			
	
