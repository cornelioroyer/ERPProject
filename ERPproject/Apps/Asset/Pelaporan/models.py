from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.Master.models import *
from datetime import datetime


class Header_asset_report(models.Model):
	no_reg = models.CharField(verbose_name='No. Laporan ', max_length=25, editable=False)
	report_add_date = models.DateField(verbose_name=_('Tanggal '), auto_now_add=True)
	asset_manager_review = models.TextField(verbose_name=_('Review Laporan '))
	asset_manager_aggrement = models.BooleanField(verbose_name=_('Persetujuan Laporan '))
		
	class Meta:
		verbose_name_plural="Header Asset Report"
		verbose_name="Header_Asset_Report"
		
	def incstring(self):
		
		try:
			data = Header_asset_report.objects.all()
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
	
	def no_req(self):
		date = datetime.now()
		now = date.strftime("%m")
		nowyear = date.strftime("%Y")
		intnow = int(now)
		intyear = int(nowyear)
		if intnow == 12:
			intnow = 1
			intyear += 1
		else : intnow += 1
		strnow = str(intnow)
		
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		nol = 5 - self.inclen()
		if nol == 1: num = "0"
		elif nol == 2: num = "00"
		elif nol == 3: num = "000"
		elif nol == 4: num = "0000"
		number = num + self.incstring()
		return 'PL/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
													'month' : strnow,
													'unik' : number}
	def save(self, force_insert=False, force_update=False, using=None):
		if self.no_reg == '':
			self.no_reg = self.no_req()
		else: self.no_reg = self.no_reg
		super(Header_asset_report, self).save()
		
	def __unicode__(self):
		return '%s' % self.no_reg
	
class Data_asset_report(models.Model):
	header = models.ForeignKey(Header_asset_report, verbose_name=_('Header Asset Report  '))
#	asset = models.ForeignKey(Ms_asset, verbose_name=_('Nama Asset '))
	choice = models.IntegerField(verbose_name=_('Pemilihan Laporan '),choices=Choice_month_report, default=2)
	start_month = models.DateField(verbose_name=_('Mulai Tanggal '))
	until_month	= models.DateField(verbose_name=_('Hingga Tanggal '))
	description = models.TextField(verbose_name=_('Deskripsi '), blank=True, null=True)
	
	class Meta:
		verbose_name_plural="Data Asset Report"
		verbose_name="Data_Asset_Report"
		
	def __unicode__(self):
		return '%s' % self.id