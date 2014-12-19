from django.db import models
from tinymce.models import HTMLField
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from Apps.Procurement.vendor.const.const import *
from datetime import datetime
from Apps.Procurement.vendor.const.const import *
from Apps.Procurement.purchaseOrder.models import Purchase_Order

class Goods_Receipt(models.Model):
	no_reg = models.CharField(verbose_name='No Reg', max_length=25, blank=True, null=True, editable=False)
	purchase_order_id = models.ForeignKey(Purchase_Order, verbose_name='No. Reg PO')
	delivery_orders = models.CharField(verbose_name='No Surat Jalan', max_length=25, blank=True, null=True)
	receipt_date = models.DateTimeField(verbose_name='Tgl Penerimaan Barang', auto_now_add=True)
	#vendor_grade = models.IntegerField(verbose_name='Nilai Vendor', choices=GRADE_CHOICES, default=2)
	vendor_grade = models.DecimalField(verbose_name='Nilai Vendor', default=0, max_digits=4, decimal_places=2, help_text='0 - 99.99')
	receipt_month = models.CharField(verbose_name='Bulan', max_length=6, editable=False)
	
	class Meta:
		verbose_name = 'Laporan Penerimaan Barang'
		verbose_name_plural = 'Laporan Penerimaan Barang'
		ordering = ['receipt_date']
	
	def print_pdf(self):
		img = '<img src="/media/static/staticproc/images/print.png" width="20%"/>'
		link = '<a href="/print_gr_admin/%(id)s/" target="blank">%(gbr)s Cetak</a>' % {'id':self.id, 'gbr':img}
		return link
	print_pdf.allow_tags = True
	print_pdf.short_description = 'Print Laporan'
	
	def receipt_m(self):
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
			data = Goods_Receipt.objects.filter(receipt_month=bln).order_by('receipt_date')
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
	
	def no_gr(self):
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
		return 'GR/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,'month' : strnow,'unik' : number}

	def denda(self):
		#now = datetime.now().utcnow().date()
		subtract = self.receipt_date.date() - self.purchase_order_id.goods_receipt_plan
		value = 0
		if int(subtract.days) >= int(self.purchase_order_id.set_of_delay.value):
			mod = int(subtract.days) % int(self.purchase_order_id.set_of_delay.value)
			subtract_min = subtract.days - mod
			bagi = float(subtract_min / int(self.purchase_order_id.set_of_delay.value))

			fine = float(bagi) * float(self.purchase_order_id.delay_fine)
			value = float(float(self.purchase_order_id.total_expenditure()) / 100) * fine
		return 'Rp %s' % value
	
	def save(self, force_insert=False, force_update=False, using=None):
		if self.no_reg is None:
			self.no_reg = self.no_gr()
		else: self.no_reg = self.no_reg
		if self.receipt_month == '':
			self.receipt_month = self.receipt_m()
		else: self.receipt_month = self.receipt_month
		super(Goods_Receipt, self).save()

	def __unicode__(self):
		return '%(ven)s' % {'ven':self.no_reg}

class Claim(models.Model):
    no_reg = models.CharField(verbose_name='No Reg', max_length=25, blank=True, null=True, editable=False)
    goods_receipt_id = models.OneToOneField(Goods_Receipt, verbose_name='No Reg Laporan Penerimaan')
    claim_add_date = models.DateTimeField(verbose_name='Tgl Buat', auto_now_add=True)
    claim_detail = HTMLField(verbose_name='Deskripsi Klaim', blank=True, null=True)
    claim_sent_date = models.DateTimeField(verbose_name='Tgl Kirim Klaim', blank=True, null=True, editable=False)
    claim_status = models.IntegerField(verbose_name='Status Klaim', choices=BR_STATUS_CHOICES)
    claim_month = models.CharField(verbose_name='Bulan', max_length=6, editable=False)

    class Meta:
        verbose_name = 'Klaim'
        verbose_name_plural = 'Klaim'
        ordering = ['claim_add_date']

    def claim_m(self):
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
            data = Claim.objects.filter(claim_month=bln).order_by('claim_add_date')
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

    def no_claim(self):
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
        return 'KLAIM/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
                                                      'month' : strnow,
                                                      'unik' : number}

    def save(self, force_insert=False, force_update=False, using=None):
        if self.no_reg is None:
            self.no_reg = self.no_claim()
        else: self.no_reg = self.no_reg
        if self.claim_status == 2:
            self.claim_sent_date = datetime.now()
        if self.claim_month == '':
            self.claim_month = self.claim_m()
        else: self.claim_month = self.claim_month
        super(Claim, self).save()

    def __unicode__(self):
        return '%(ven)s' % {'ven':self.no_reg}
