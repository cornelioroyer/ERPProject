from django.db import models
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from Apps.Procurement.vendor.const.const import *
from datetime import datetime
from django.core.urlresolvers import reverse
from Apps.Procurement.property.models import Goods_Type, Currency, Fields, Sub_Fields, Classification, Unit_Of_Measure
from Apps.Procurement.internal.models import Data_Purchase_Request, Data_Rush_Order
from Apps.Procurement.vendor.models import Ms_Vendor

from Apps.Hrm.Master_General.models import Department
from Apps.Accounting.CashBank.models import Budget

from django.template.defaultfilters import slugify

class Announcement_Proc(models.Model):
	title = models.CharField(max_length=50, verbose_name='Judul')
	data_purchase_request = models.OneToOneField(Data_Purchase_Request, verbose_name='ID Item dari PP, atau*', blank=True, null=True,
												help_text='*) Masukkan salah satu ID Item PP atau ID Item RO')
	data_rush_order = models.OneToOneField(Data_Rush_Order, verbose_name='ID Item dari RO*', blank=True, null=True, 
											help_text='*) Jika keduanya diisi maka yang akan disimpan hanya ID Item PP')
	slug = models.SlugField(unique=True, max_length=50, verbose_name='Link', help_text='nama yg dipakai untuk link', blank=True,editable=False)
	classification = models.ForeignKey(Classification, verbose_name='Klasifikasi')
	fields = models.ForeignKey(Fields, verbose_name='Bidang')
	sub_fields = models.ForeignKey(Sub_Fields, verbose_name='Sub Bidang')
	detail_proc = HTMLField(verbose_name='Detail Pengadaan')
	proc_budget = models.DecimalField(decimal_places=2,max_digits=20,verbose_name='Anggaran', blank=True, null=True)
	winner_determination = models.CharField(max_length=10, choices = PENENTUAN_PEMENANG_CHOICES, verbose_name='Penentuan Pemenang')
	proc_doc = models.FileField(upload_to='uploads/dokproc', verbose_name='Dokumen')
	proc_add_date = models.DateTimeField(auto_now_add=True, verbose_name='Tgl Buat')
	end_enlisting = models.DateTimeField(verbose_name='Tgl Batas Pendaftaran')
	end_bid = models.DateTimeField(verbose_name='Tgl Batas Penawaran')
	end_expostulating = models.DateTimeField(verbose_name='Tgl Batas Masa Sanggah')
	published = models.BooleanField(default=True, verbose_name='Published?')
	winner = models.ForeignKey(Ms_Vendor, verbose_name='Pemenang*', blank=True, null=True, help_text='*) Masukkan pemenang jika metode penentuannya manual')
	
	class Meta:
		verbose_name = 'Pengumuman Pengadaan'
		verbose_name_plural = 'Pengumuman Pengadaan'
		ordering = ['-proc_add_date']

	def detail_procx(self):
		return '%s' % self.detail_proc
	detail_procx.allow_tags = True
	detail_procx.short_description = 'Deskripsi Pengadaan'
	
	def status(self):
		now = datetime.now().utcnow().date()
		now_t = datetime.now().utcnow().time()
		end_sign = self.end_enlisting.date()
		end_sign_t = self.end_enlisting.time()
		end_bid = self.end_bid.date()
		end_bid_t = self.end_bid.time()
		end_exp = self.end_expostulating.date()
		end_exp_t = self.end_expostulating.time()
		status = 'Selesai'
		daftar = end_sign-now
		tawar = end_bid-now
		sanggah = end_exp-now
		
		if sanggah.days == 0:
			if now_t < end_exp_t:
				status = 'Masa Sanggah'
		if sanggah.days > 0:
			status = 'Masa Sanggah'
		
		if tawar.days == 0:
			if now_t < end_bid_t:
				status = 'Penawaran'
		if tawar.days > 0:
			status = 'Penawaran'
		
		if daftar.days == 0:
			if now_t < end_sign_t:
				status = 'Pendaftaran'
		if daftar.days > 0:
			status = 'Pendaftaran'
		return status
		
	def winner_m(self):
		txt = 'Pelelangan masih dalam pelaksanaan'
		if self.winner_determination == 'otomatis':
			max = 0
			who = ' '
			try:
				data = Vendor_Proc.objects.filter(announcement_proc__id=self.id)
				for d in data:
					if d.bid_value > max:
						max = d.bid_value
				win = Vendor_Proc.objects.filter(bid_value=max)
				for w in win:
					who += w.ms_vendor.vendor_name+','
			except:
				pass
			if self.status() == 'Selesai':
				txt = 'Pemenang Pelelangan: %(w)s dengan nilai penawaran Rp %(m)s' % {'w':who,'m':max}
		else:
			if self.status() == 'Selesai':
				try:
					win = Vendor_Proc.objects.get(id=self.winner__id)
					txt = 'Pemenang Pelelangan: %(w)s , dengan nilai penawaran Rp %(m)s' % {'w':self.winner__vendor_name,'m':win.bid_value}
				except:
					txt = 'Pemenang Belum ditentukan'
			pass
		return txt
	winner_m.short_description = 'Pemenang'
	
	def get_absolute_url(self):
		return reverse('Apps.Procurement.vendor.views.post', args=[self.slug])
	
	def save(self, force_insert=False, force_update=False, using=None):
		self.slug = slugify(self.title)
		if self.data_purchase_request is not None and self.data_rush_order is not None:
			self.data_purchase_request = self.data_purchase_request
			self.data_rush_order = None
		super(Announcement_Proc, self).save()
	
	def __unicode__(self):
		return 'ID: %(id)s | %(title)s' % {'id':self.id,'title':self.title}

class Vendor_Proc(models.Model):
	ms_vendor = models.ForeignKey(Ms_Vendor, verbose_name='Vendor')
	announcement_proc = models.ForeignKey(Announcement_Proc, verbose_name='Pengumuman Lelang')
	bid_value = models.DecimalField(verbose_name='Nilai Penawaran', max_digits=15, decimal_places=2, blank=True, null=True)
	doc_bid = models.FileField(upload_to='uploads/dokvendor/dokbid',verbose_name='Dokumen Penawaran', blank=True, null=True)
	
	class Meta:
		verbose_name = 'Penawaran Vendor'
		verbose_name_plural = 'Penawaran Vendor'
		ordering = ['-announcement_proc__proc_add_date']
	
	def __unicode__(self):
		return '%(ven)s | %(val)s' % {'ven':self.ms_vendor.vendor_name, 'val':self.bid_value}

class Bidding_Proc(models.Model):
	vendor_proc = models.ForeignKey(Vendor_Proc, verbose_name='ID Penawaran Vendor')
	msg_add_date = models.DateTimeField(auto_now_add=True,verbose_name='Tgl Kirim Pesan', editable=False)
	uname = models.CharField(max_length=50,verbose_name='Pengirim', default='admin')
	message = HTMLField(verbose_name='Isi Pesan')
	
	class Meta:
		verbose_name = 'Pesan Penawaran'
		verbose_name_plural = 'Pesan Penawaran'
		ordering = ['-msg_add_date']
	
	def msg(self):
		return '%s' % self.message
	msg.allow_tags = True
	msg.short_description = 'Isi Pesan'
	
	def __unicode__(self):
		return u'%s' % self.id
