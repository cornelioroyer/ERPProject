from django.db import models
from tinymce.models import HTMLField
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import signals
from Apps.Procurement.vendor.const.const import *
from django.utils.translation import ugettext as _
from datetime import datetime
from Apps.Procurement.purchaseOrder.models import Purchase_Order
from Apps.Procurement.property.models import Goods_Type, Currency, Fields, Sub_Fields, Classification, Unit_Of_Measure

from Apps.Accounting.CashBank.models import Budget
from Apps.Accounting.GeneralLedger.models import Ms_Fiscal_Years
from Apps.Hrm.Master_General.models import Department

class User_Intern(models.Model):
	intern_name = models.CharField(max_length=50, verbose_name='Nama Lengkap')
	username = models.CharField(max_length=50, unique=True)
	password = models.CharField(max_length=50)
	intern_occupation = models.CharField(max_length=30, verbose_name='Jabatan')
	intern_date_register = models.DateField(auto_now_add=True, verbose_name='Tgl Terdaftar')
	access_level = models.CharField(max_length=30, choices=LEVEL_AKSES_CHOICES, verbose_name='Hak Akses')
	department = models.ForeignKey(Department,verbose_name='Departemen')
	intern_verified = models.BooleanField(default=False, verbose_name='Verified?')
	
	class Meta:
		verbose_name = 'User Internal'
		verbose_name_plural = 'User Internal'
		ordering = ['id']
	
	def __unicode__(self):
		return '%s' % self.username

class Role_User(models.Model):
	user = models.OneToOneField(User, related_name=_('User'))
	access_level = models.CharField(max_length=30, choices=LEVEL_AKSES_CHOICES, verbose_name='Level Akses', blank=True, null=True)
	
	class Meta:
		verbose_name = 'Hak Akses'
		verbose_name_plural = 'Hak Akses'
		ordering = ['id']
	
	def __unicode__(self):
		return "%s" % self.user

def create_user_profile(sender, instance, created, **kwargs):  
	if created == True:  
		profile, created = Role_User.objects.get_or_create(user=instance)
        
post_save.connect(create_user_profile, sender=User)

class Header_Plan(models.Model):
    #no_reg = models.CharField(_('No. Reg. '), max_length=30)
	no_reg = models.CharField(verbose_name='No Reg', max_length=25, blank=True, null=True, editable=False)
	department = models.ForeignKey(Department, verbose_name='Departemen')
	plan_add_date = models.DateTimeField(verbose_name='Tgl Buat', auto_now_add=True)
	lock = models.BooleanField(default=False)
	plan_month = models.CharField(max_length=6, editable=False)
	fiscal_year = models.ForeignKey(Ms_Fiscal_Years, verbose_name='Tahun Fiscal')
	
	class Meta:
		verbose_name = 'Header RKB'
		verbose_name_plural = 'Header RKB'
		ordering = ['-id']
	
	def incstring(self):
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
		nowyear = str(intyear)
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bln = '%(y)s%(m)s' % {'y':nowyear,'m':strnow}
		jml=0
		try:
			data = Header_Plan.objects.filter(plan_month=bln).order_by('plan_add_date')
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
	
	def no_plan(self):
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
		return '%(prefix)s/%(year)s/%(month)s/%(unik)s' % {'prefix' : RKB_REG_PREFIX,
                                                           'year' : intyear,
                                                           'month' : strnow,
                                                           'unik' : number}
	
	def plan_m(self):
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
		
		return '%(year)s%(month)s' % {'year':intyear, 'month':strnow}
	
	def get_absolute_url(self):
		return reverse('Apps.Procurement.internal.views.lock_rkb', args=[self.id])
	
	def save(self, force_insert=False, force_update=False, using=None):
		if self.no_reg is None:
			self.no_reg = self.no_plan()
		else: self.no_reg = self.no_reg
		if self.plan_month == '':
			self.plan_month = self.plan_m()
		else: self.plan_month = self.plan_month
		super(Header_Plan, self).save()
	
	def __unicode__(self):
		strid = str(self.no_reg)
		return u'%s' % strid

class Data_Plan(models.Model):
	header_plan_id = models.ForeignKey(Header_Plan, verbose_name='ID Header')
	plan_goods_name = models.CharField(verbose_name='Nama Brg', max_length = 40)
	goods_type_id = models.ForeignKey(Goods_Type, verbose_name='Jenis Brg')
	unit_of_measure_id = models.ForeignKey(Unit_Of_Measure, verbose_name='Satuan')
	plan_used = models.DateField(verbose_name='Rencana Pakai')
	plan_amount = models.IntegerField(verbose_name='Rencana Beli')
	currency_id = models.ForeignKey(Currency, verbose_name='Mata Uang')
	plan_unit_price = models.DecimalField(verbose_name='Harga Satuan',null=True, decimal_places=2, max_digits=15)
	plan_total_rupiah = models.DecimalField(verbose_name='Jumlah',blank=True,null=True, editable=False, decimal_places=2, max_digits=15)
	plan_total_price = models.DecimalField(verbose_name='Total Harga',blank=True,null=True, editable=False, decimal_places=2, max_digits=15)
	plan_detail = models.CharField(verbose_name='Keterangan', max_length = 40)
	
	class Meta:
		verbose_name = 'Data RKB'
		verbose_name_plural = 'Data RKB'
		ordering = ['-id']
	
	def url_edit(self):
		return reverse('Apps.Procurement.internal.views.edit_rkb', args=[self.id])
	
	def url_delete(self):
		return reverse('Apps.Procurement.internal.views.del_rkb', args=[self.id])
	
	def tot_rupiah(self):
		currency = Currency.objects.get(currency_symbol=self.currency_id.currency_symbol)
		total_rp = float(self.plan_unit_price) * float(currency.currency_rate)
		return total_rp
	
	def tot_price(self):
		total_price = float(self.plan_amount) * float(self.tot_rupiah())
		return total_price
	
	def save(self, force_insert=False, force_update=False, using=None):
		self.plan_total_rupiah = self.tot_rupiah()
		self.plan_total_price = self.tot_price()
		super(Data_Plan, self).save()
	
	def __unicode__(self):
		return u'%s' % self.id

class Header_Purchase_Request(models.Model):
	no_reg = models.CharField(verbose_name='No Reg', max_length=25, editable=False)
	department = models.ForeignKey(Department, verbose_name='Departemen')
	request_add_date = models.DateTimeField(verbose_name='Tgl Buat', auto_now_add=True)
	request_month = models.CharField(verbose_name='Bulan', max_length=6)
	warehouse_review = HTMLField(verbose_name='Review Gudang', blank=True)
	financial_review = HTMLField(verbose_name='Review Keuangan', blank=True)
	procurement_review = HTMLField(verbose_name='Review Procurement', blank=True)
	request_lock = models.BooleanField(default=False)
	request_lock_date = models.DateField(verbose_name='Tgl Kunci', blank=True, null=True)
	warehouse_agreement = models.BooleanField(default=False, verbose_name='Persetujuan Gudang')
	financial_agreement = models.BooleanField(default=False, verbose_name='Persetujuan Financial')
	procurement_agreement = models.BooleanField(default=False, verbose_name='Persetujuan Procurement')
	header_plan = models.ForeignKey(Header_Plan, verbose_name='ID RKB')
	fiscal_year = models.ForeignKey(Ms_Fiscal_Years, verbose_name='Tahun Fiscal', editable=False)
	
	class Meta:
		verbose_name = 'Header PP'
		verbose_name_plural = 'Header PP'
		ordering = ['id']
	
	def w_rev(self):
		return '%s' % self.warehouse_review
	w_rev.allow_tags = True
	w_rev.short_description = 'Review Gudang'
	
	def f_rev(self):
		return '%s' % self.financial_review
	f_rev.allow_tags = True
	f_rev.short_description = 'Review Financial'
	
	def p_rev(self):
		return '%s' % self.procurement_review
	p_rev.allow_tags = True
	p_rev.short_description = 'Review Procurement'
	
	def incstring(self):
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
		nowyear = str(intyear)
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bln = '%(y)s%(m)s' % {'y':nowyear,'m':strnow}
		jml=0
		try:
			data = Header_Purchase_Request.objects.filter(request_month=bln).order_by('request_add_date')
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
		return 'PP/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
													'month' : strnow,
													'unik' : number}
		
	def total_expenditure(self):
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intyear += 1
		
		total_all1 = 0		
		
		try:
			budget = Budget.objects.filter(department=self.department, year__Code=str(intyear))
			budget_ada = budget.count()
		except:
			pass
		
		for bs in budget:
			b_id = bs.id
			b_value = bs.budget_value
			b_devided = bs.budget_devided
		
		bagi = int(b_value) / int(b_devided)
		n = x = 1
		dr = Data_Purchase_Request.objects.filter(header_purchase_request_id=self.id)
		for drs in dr:
			total_all1 += float(drs.request_total_price)
		return total_all1
	total_expenditure.short_description = _('Total Pengeluaran')
	
	def saldo(self):
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intnow = 1
			intyear += 1
		else :
			intnow += 1
		
		periode = total_all = 0		
		
		try:
			budget = Budget.objects.filter(department=self.department, year__Code=str(intyear))
			budget_ada = budget.count()
		except:
			pass
		
		for bs in budget:
			b_value = bs.budget_value
			b_devided = bs.budget_devided
		
		bagi = int(b_value) / int(b_devided)
		bagian = 12 / int(b_devided)
		n = 1
		while n <= int(b_devided):
			temp = int(bagian) * n
			temp2 = (temp - int(bagian))+1
			if intnow <= temp and intnow >= temp2:
				periode = n
				while temp2 <= temp:
					strtemp2 = str(temp2)
					strnow = strtemp2
					if len(strtemp2) < 2 :
						strnow = '0%(strtemp2)s' % {'strtemp2' : strtemp2}
					bln = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
					try: 
						dr = Data_Purchase_Request.objects.filter(header_purchase_request_id__department=self.department, header_purchase_request_id__request_month=bln)
						for drs in dr:
							total_all += float(drs.request_total_price)
					except:
						pass
					
					try:
						dro = Data_Rush_Order.objects.filter(header_rush_order_id__department=self.department, header_rush_order_id__ro_month=bln, 
							header_rush_order_id__ro_lock=True)
						for dros in dro:
							total_all += float(dros.ro_total_price)
					except:
						pass
					temp2 = temp2 + 1
					
			n = n + 1
		sisa = float(bagi) - total_all
		
		return 'sisa Rp %(sisa)s' % {'sisa':sisa}
		#return '%(ss)s' % {'ss':bagian}
	saldo.short_description = _('Saldo per Periode')
	
	def get_absolute_url(self):
		return reverse('Apps.Procurement.internal.views.lock_pp', args=[self.id])
	
	def save(self, force_insert=False, force_update=False, using=None):
		if self.no_reg == '':
			self.no_reg = self.no_req()
		else: self.no_reg = self.no_reg
		if self.warehouse_agreement == True and self.financial_agreement == True and self.procurement_agreement == True:
			self.request_lock = True
			self.request_lock_date = datetime.now()
		super(Header_Purchase_Request, self).save()
	
	def __unicode__(self):
		strid = str(self.no_reg)
		return u'%s' % strid

class Data_Purchase_Request(models.Model):
	header_purchase_request_id = models.ForeignKey(Header_Purchase_Request, verbose_name='ID Header', blank=True, null=True,default=None)
	no_item = models.CharField(verbose_name='No Item', max_length=25, editable=False)
	request_goods_name = models.CharField(verbose_name='Nama Brg', max_length = 40)
	goods_type_id = models.ForeignKey(Goods_Type, verbose_name='Jenis Brg')
	unit_of_measure_id = models.ForeignKey(Unit_Of_Measure, verbose_name='Satuan')
	request_used = models.DateField(verbose_name='Rencana Pakai')
	request_amount = models.IntegerField(verbose_name='Rencana Beli')
	currency_id = models.ForeignKey(Currency, verbose_name='Mata Uang')
	request_unit_price = models.DecimalField(verbose_name='Harga Satuan', decimal_places=2, max_digits=15)
	request_total_rupiah = models.DecimalField(verbose_name='Jumlah',blank=True, null=True, decimal_places=2, max_digits=15,editable=False)
	request_total_price = models.DecimalField(verbose_name='Total Harga',blank=True, null=True, decimal_places=2, max_digits=15,editable=False)
	request_detail = models.CharField(verbose_name='Keterangan', max_length = 40, blank=True)
	no_po = models.ForeignKey(Purchase_Order, verbose_name='Purchase Order', blank=True, null=True)
	state_choices = models.IntegerField(max_length=1, choices=PP_STATE_CHOICES, blank=True, null=True)
	method_choices = models.IntegerField(max_length=1, choices=PP_METHOD_CHOICES, blank=True, null=True)
	
	class Meta:
		verbose_name = 'Data PP'
		verbose_name_plural = 'Data PP'
		ordering = ['-id']
	
	def url_edit(self):
		return reverse('Apps.Procurement.internal.views.edit_pp', args=[self.id])
	
	def url_delete(self):
		return reverse('Apps.Procurement.internal.views.del_pp', args=[self.id])
	
	def tot_rupiah(self):
		currency = Currency.objects.get(currency_symbol=self.currency_id.currency_symbol)
		total_rp = float(self.request_unit_price) * float(currency.currency_rate)
		return total_rp
	
	def tot_price(self):
		total_price = float(self.request_amount) * float(self.tot_rupiah())
		return total_price
	
	def incstring(self):
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
		nowyear = str(intyear)
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bln = '%(y)s%(m)s' % {'y':nowyear,'m':strnow}
		jml=0
		try:
			data = Data_Purchase_Request.objects.filter(header_purchase_request_id__request_month=bln)
			jml = data.count()
		except:
			jml=0
			pass
		no = 0
		if jml == 0:
			no = 0
		else: 
			for d in data:
				split = str(d.no_item).split('/')
				no = int(split[3])
		num = no + 1
		cstring = str(num)
		return cstring
	
	def inclen(self):
		leng = len(self.incstring())
		return leng
	
	def no_brg(self):
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
		return 'ITEM/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
													'month' : strnow,
													'unik' : number}
	
	def save(self, force_insert=False, force_update=False, using=None):
		self.request_total_rupiah = self.tot_rupiah()
		self.request_total_price = self.tot_price()
		if self.no_item == '':
			self.no_item = self.no_brg()
		else: self.no_item = self.no_item
		super(Data_Purchase_Request, self).save()
	
	def __unicode__(self):
		return u'%s' % self.no_item

class Header_Rush_Order(models.Model):
	no_reg = models.CharField(verbose_name='No Reg', max_length=25, editable=False)
	department = models.ForeignKey(Department, verbose_name='Departemen')
	ro_add_date = models.DateTimeField(verbose_name='Tgl Buat', auto_now_add=True)
	ro_month = models.CharField(verbose_name='Bulan', max_length=6, editable=False)
	warehouse_review = HTMLField(verbose_name='Review Gudang', blank=True)
	financial_review = HTMLField(verbose_name='Review Keuangan', blank=True)
	procurement_review = HTMLField(verbose_name='Review Procurement', blank=True)
	ro_sent = models.BooleanField(default=False)
	ro_lock = models.BooleanField(default=False)
	ro_lock_date = models.DateField(verbose_name='Tgl Kunci', blank=True, null=True)
	warehouse_agreement = models.BooleanField(default=False, verbose_name='Persetujuan Gudang')
	financial_agreement = models.BooleanField(default=False, verbose_name='Persetujuan Financial')
	procurement_agreement = models.BooleanField(default=False, verbose_name='Persetujuan Procurement')
	ro_type = models.IntegerField(max_length=1, choices=RO_STATUS_CHOICES, default=2, editable=False)
	fiscal_year = models.ForeignKey(Ms_Fiscal_Years, verbose_name='Tahun Fiscal')
	
	class Meta:
		verbose_name = 'Header RO'
		verbose_name_plural = 'Header RO'
		ordering = ['id']
	
	def w_rev(self):
		return '%s' % self.warehouse_review
	w_rev.allow_tags = True
	w_rev.short_description = 'Review Gudang'
	
	def f_rev(self):
		return '%s' % self.financial_review
	f_rev.allow_tags = True
	f_rev.short_description = 'Review Financial'
	
	def p_rev(self):
		return '%s' % self.procurement_review
	p_rev.allow_tags = True
	p_rev.short_description = 'Review Procurement'
	
	def incstring(self):
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
		nowyear = str(intyear)
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bln = '%(y)s%(m)s' % {'y':nowyear,'m':strnow}
		jml=0
		try:
			data = Header_Rush_Order.objects.filter(ro_month=bln).order_by('ro_add_date')
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
		return 'RO/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
													'month' : strnow,
													'unik' : number}
		
	def total_expenditure(self):
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intyear += 1
		
		total_all1 = 0		
		
		try:
			budget = Budget.objects.filter(department=self.department, year__Code=str(intyear))
			budget_ada = budget.count()
		except:
			pass
		
		for bs in budget:
			b_id = bs.id
			b_value = bs.budget_value
			b_devided = bs.budget_devided
		
		bagi = int(b_value) / int(b_devided)
		n = x = 1
		dr = Data_Rush_Order.objects.filter(header_rush_order_id=self.id)
		for drs in dr:
			total_all1 += float(drs.ro_total_price)
		return total_all1
	total_expenditure.short_description = _('Total Pengeluaran')
	
	def saldo(self):
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intnow = 1
			intyear += 1
		else :
			intnow += 1
		
		periode = total_all = 0		
		
		try:
			budget = Budget.objects.filter(department=self.department, year__Code=str(intyear))
			budget_ada = budget.count()
		except:
			pass
		
		for bs in budget:
			b_value = bs.budget_value
			b_devided = bs.budget_devided
		
		bagi = int(b_value) / int(b_devided)
		bagian = 12 / int(b_devided)
		n = 1
		while n <= int(b_devided):
			temp = int(bagian) * n
			temp2 = (temp - int(bagian))+1
			if intnow <= temp and intnow >= temp2:
				periode = n
				while temp2 <= temp:
					strtemp2 = str(temp2)
					strnow = strtemp2
					if len(strtemp2) < 2 :
						strnow = '0%(strtemp2)s' % {'strtemp2' : strtemp2}
					bln = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
					try: 
						dr = Data_Purchase_Request.objects.filter(header_purchase_request_id__department=self.department, header_purchase_request_id__request_month=bln)
						for drs in dr:
							total_all += float(drs.request_total_price)
					except:
						pass
					try:
						dro = Data_Rush_Order.objects.filter(header_rush_order_id__department=self.department, header_rush_order_id__ro_month=bln, 
							header_rush_order_id__ro_lock=True)
						for dros in dro:
							total_all += float(dros.ro_total_price)
					except:
						pass
					temp2 = temp2 + 1
					
			n = n + 1
		sisa = float(bagi) - total_all
		
		return 'sisa Rp %(sisa)s' % {'sisa':sisa}
		#return '%(ss)s' % {'ss':bagian}
	saldo.short_description = _('Saldo per Periode')
	
	def bln(self):
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intnow = 1
			intyear += 1
		else : 
			intnow += 1
		
		strnow = str(intnow)
		
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bulan = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
		return bulan
	
	def save(self, force_insert=False, force_update=False, using=None):
		if self.no_reg == '':
			self.no_reg = self.no_req()
		else: self.no_reg = self.no_reg
		if self.ro_month == '':
			self.ro_month = self.bln()
		else: self.ro_month = self.ro_month
		if self.warehouse_agreement == True and self.financial_agreement == True and self.procurement_agreement == True:
			self.ro_lock = True
			self.ro_lock_date = datetime.now()
		super(Header_Rush_Order, self).save()
	
	def __unicode__(self):
		strid = str(self.no_reg)
		return u'%s' % strid

class Data_Rush_Order(models.Model):
	header_rush_order_id = models.ForeignKey(Header_Rush_Order, verbose_name='ID Header', blank=True, null=True,default=None)
	no_item = models.CharField(verbose_name='No Item', max_length=25, editable=False)
	ro_goods_name = models.CharField(verbose_name='Nama Brg', max_length = 40)
	goods_type_id = models.ForeignKey(Goods_Type, verbose_name='Jenis Brg')
	unit_of_measure_id = models.ForeignKey(Unit_Of_Measure, verbose_name='Satuan')
	ro_used = models.DateField(verbose_name='Rencana Pakai')
	ro_amount = models.IntegerField(verbose_name='Rencana Beli')
	currency_id = models.ForeignKey(Currency, verbose_name='Mata Uang')
	ro_unit_price = models.DecimalField(verbose_name='Harga Satuan', decimal_places=2, max_digits=15)
	ro_total_rupiah = models.DecimalField(verbose_name='Jumlah',blank=True, null=True, decimal_places=2, max_digits=15,editable=False)
	ro_total_price = models.DecimalField(verbose_name='Total Harga',blank=True, null=True, decimal_places=2, max_digits=15,editable=False)
	ro_detail = models.CharField(verbose_name='Keterangan', max_length = 40, blank=True)
	no_po = models.ForeignKey(Purchase_Order, verbose_name='Purchase Order', blank=True, null=True)
	state_choices = models.IntegerField(max_length=1, choices=PP_STATE_CHOICES, blank=True, null=True)
	method_choices = models.IntegerField(max_length=1, choices=PP_METHOD_CHOICES, blank=True, null=True)
	
	class Meta:
		verbose_name = 'Data RO'
		verbose_name_plural = 'Data RO'
		ordering = ['id']
	
	def url_edit(self):
		return reverse('Apps.Procurement.internal.views.edit_ro', args=[self.id])
	
	def url_delete(self):
		return reverse('Apps.Procurement.internal.views.del_ro', args=[self.id])
	
	def tot_rupiah(self):
		currency = Currency.objects.get(currency_symbol=self.currency_id.currency_symbol)
		total_rp = float(self.ro_unit_price) * float(currency.currency_rate)
		return total_rp
	
	def tot_price(self):
		total_price = float(self.ro_amount) * float(self.tot_rupiah())
		return total_price
	
	def incstring(self):
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
		nowyear = str(intyear)
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bln = '%(y)s%(m)s' % {'y':nowyear,'m':strnow}
		jml=0
		try:
			data = Data_Rush_Order.objects.filter(header_rush_order_id__ro_month=bln)
			jml = data.count()
		except:
			jml=0
			pass
		no = 0
		if jml == 0:
			no = 0
		else: 
			for d in data:
				split = str(d.no_item).split('/')
				no = int(split[3])
		num = no + 1
		cstring = str(num)
		return cstring
	
	def inclen(self):
		leng = len(self.incstring())
		return leng
	
	def no_brg(self):
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
		return 'ITEMRO/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
													'month' : strnow,
													'unik' : number}
	
	def save(self, force_insert=False, force_update=False, using=None):
		self.ro_total_rupiah = self.tot_rupiah()
		self.ro_total_price = self.tot_price()
		if self.no_item == '':
			self.no_item = self.no_brg()
		else: self.no_item = self.no_item
		super(Data_Rush_Order, self).save()
	
	def __unicode__(self):
		return u'%s' % self.no_item
