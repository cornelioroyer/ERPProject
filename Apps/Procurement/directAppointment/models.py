from django.db import models
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from Apps.Procurement.vendor.const.const import *
from datetime import datetime
from Apps.Procurement.internal.models import Data_Purchase_Request, Data_Rush_Order
from Apps.Procurement.vendor.models import Ms_Vendor

class Bidding_Request(models.Model):
	no_reg = models.CharField(verbose_name='No Reg', max_length=25, blank=True, null=True, editable=False)
	ms_vendor = models.ForeignKey(Ms_Vendor, verbose_name='Vendor')
	br_detail = HTMLField(verbose_name='Detail Pengadaan')
	br_add_date = models.DateTimeField(verbose_name='Tgl Buat', auto_now_add=True)
	br_end_date = models.DateTimeField(verbose_name='Tgl Selesai')
	br_sent_date = models.DateTimeField(verbose_name='Tgl Kirim', editable=False, null=True, blank=True)
	br_status = models.IntegerField(verbose_name='Status Request', max_length=1, choices=BR_STATUS_CHOICES) 
	bid_value = models.DecimalField(verbose_name='Nilai Penawaran', max_digits=15, decimal_places=2, blank=True, null=True)
	br_message = HTMLField(verbose_name='Balasan', blank=True, null=True)
	br_month = models.CharField(verbose_name='Bulan', max_length=6, editable=False)
	
	class Meta:
		verbose_name = 'Permintaan Penawaran'
		verbose_name_plural = 'Permintaan Penawaran'
		ordering = ['-br_add_date']
	
	def br_m(self):
		date = datetime.now()
		now = date.strftime("%m")
		nowyear = date.strftime("%Y")
		intnow = int(now)
		intyear = int(nowyear)
		strnow = str(intnow)
		
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		else: strnow = '%(strnow)s' % {'strnow' : strnow}
		bln = '%(y)s%(m)s' % {'y':intyear,'m':strnow}
		return bln
	
	def incstring(self):
		date = datetime.now()
		now = date.strftime("%m")
		nowyear = date.strftime("%Y")
		intnow = int(now)
		intyear = int(nowyear)
		strnow = str(intnow)
		nowyear = str(intyear)
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bln = '%(y)s%(m)s' % {'y':nowyear,'m':strnow}
		jml=0
		try:
			data = Bidding_Request.objects.filter(br_month=bln).order_by('br_add_date')
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
	
	def no_br(self):
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
		return 'PerPen/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
													'month' : strnow,
													'unik' : number}
	
	def status(self):
		now = datetime.now().utcnow().date()
		now_t = datetime.now().utcnow().time()
		end_date = self.br_end_date.date()
		end_date_t = self.br_end_date.time()
		status = 'Selesai'
		tawar = end_date-now
		
		if tawar.days == 0:
			if now_t < end_date_t:
				status = 'Penawaran'
		if tawar.days > 0:
			status = 'Penawaran'
		return status
	
	def br_detailx(self):
		return '%s' % self.br_detail
	br_detailx.allow_tags = True
	br_detailx.short_description = 'Deskripsi Pengadaan'
	
	def print_pdf(self):
		img = '<img src="/media/static/staticproc/images/print.png" width="20%"/>'
		link = '<a href="/print_rq_admin/%(id)s/" target="blank">%(gbr)s Cetak</a>' % {'id':self.id, 'gbr':img}
		return link
	print_pdf.allow_tags = True
	print_pdf.short_description = 'Print RQ'
	
	def save(self, force_insert=False, force_update=False, using=None):
		if self.no_reg is None:
			self.no_reg = self.no_br()
		else: self.no_reg = self.no_reg
		if self.br_status == 2:
			self.br_sent_date = datetime.now()
		if self.br_month == '':
			self.br_month = self.br_m()
		else: self.br_month = self.br_month
		super(Bidding_Request, self).save()
	
	def __unicode__(self):
		return '%(ven)s' % {'ven':self.no_reg}

class Bidding_Request_Item(models.Model):
	bidding_request = models.ForeignKey(Bidding_Request, verbose_name='ID Bidding')
	data_purchase_request = models.OneToOneField(Data_Purchase_Request, verbose_name='ID Item PP', null=True, blank=True,
							help_text='Masukkan ID PP atau RO (salah satu saja)')
	data_rush_order = models.ForeignKey(Data_Rush_Order, null=True, blank=True, verbose_name='ID Item RO',
							help_text='*) Jika ID Item PP dan ID Item RO diisi keduanya, maka yang disimpan hanya ID Item PP')
	
	class Meta:
		verbose_name = 'Item Permintaan Penawaran'
		verbose_name_plural = 'Item Permintaan Penawaran'
		ordering = ['-bidding_request__br_add_date']
	
	def save(self, force_insert=False, force_update=False, using=None):
		if self.data_purchase_request is not None and self.data_rush_order is not None:
			self.data_purchase_request = self.data_purchase_request
			self.data_rush_order = None
		super(Bidding_Request_Item, self).save()
	
	def __unicode__(self):
		return u'%s' % self.id