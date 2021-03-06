from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.const import *
from Apps.Asset.Master.models import *
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import Department, Section
from Apps.Hrm.Data_Personel_Management.models import Employee, Position
from datetime import datetime
from tinymce.models import HTMLField

class Header_user_request(models.Model):
	no_reg = models.CharField(verbose_name='No Reg Header', max_length=25, editable=False)
	department = models.ForeignKey(Department, verbose_name=_('Nama Departement  '), help_text='Langsung Pilih Menu Simpan')
	user = models.ForeignKey(Employee,verbose_name='Nama Pegawai', max_length=50)
	req_date = models.DateField(verbose_name=_('Tanggal '), auto_now_add=True)
	department_staff_aggreement = models.BooleanField(verbose_name =_('Dikirim '), default=False, help_text='Jangan Dikirim Dulu Sebelum Jawaban Penanganan Dimasukkan ')
		
	class Meta:
		verbose_name_plural="Header User Request"
		verbose_name= "Header_User_Request"
	
	def incstring(self):
		try:
			data = Header_user_request.objects.all()
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
		return 'PR/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
	
	def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
		if self.no_reg =='':
			self.no_reg = self.no_rek()
		else:
			self.no_reg = self.no_reg
		super(Header_user_request, self).save()
		
	def __str__(self):
		return '%(no_reg)s | %(department)s' % {'no_reg':self.no_reg,'department':self.department}
		
	

    
class Data_user_request(models.Model):
	header = models.ForeignKey(Header_user_request, verbose_name=_('No. Reg Header '))
	asset = models.ForeignKey(Ms_asset, verbose_name=('Asset '), blank=True, null=True, help_text=')* Isi Asset jika ingin melakukan Permintaan Perbaikan saja')
	choice_service = models.IntegerField(verbose_name=_('Permintaan  '),choices=Pilihan_request)	
	date_used = models.DateField(verbose_name=_('Tanggal Penggunaan '))
	answer_service = models.IntegerField(verbose_name=_('Jawaban Penanganan  '), choices=Pilihan_service, blank=True, null=True, max_length=1)		
	description = HTMLField(verbose_name=_('Detail Permintaan '), blank=True , help_text='Kriteria Permintaan ')
	asset_reply = HTMLField(verbose_name=_('Asset Staff Review '), blank=True)
	
	class Meta:
		verbose_name_plural="Data User Request"
        verbose_name= "Data_User_Request"
		
	def descriptionx(self):
		return '%s' % self.description
	descriptionx.allow_tags = True
	descriptionx.short_description = 'Detail Permintaan'
	
	def asset_replyx(self):
		return '%s' % self.asset_reply
	asset_replyx.allow_tags = True
	asset_replyx.short_description = 'Asset Staff Review'
	
	def ID(self):
		srv = ''
		if self.answer_service == 11:
			srv = 'Pengadaan'
		elif self.answer_service == 2:
			srv = 'Perbaikan'
		elif self.answer_service == 13:
			srv = 'Penggantian'
		elif self.answer_service == 4:
			srv = 'Pemindahan'
		elif self.answer_service == 5:
			srv = 'Peminjaman'
		elif self.answer_service == 6:
			srv = 'Penghapusan'
		elif self.answer_service == 7:
			srv = 'Ditolak'
		else:
			srv = '----'
		
		return u' Request Number/ %(id)s | %(choice_service)s' % {'id':self.id,'choice_service':srv}
	ID.short_description='ID'
	
	#u'Request Number | %(id)s' % {'id':self.id}
	
	def __unicode__(self):
		return '%s' % self.ID()
	
	#u' Req Num %(id)s | %(choice_service)s' % {'id':self.id, 'choice_service':self.choice_service}

	
    
    	

