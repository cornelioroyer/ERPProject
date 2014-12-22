from django.db import models
from django.utils.translation import ugettext as _
from Apps.Manufacturing.const import *
#from Apps.Manufacturing.MasterData.models import *
#from Apps.Manufacturing.ProductionPlanning.models import *
from datetime import datetime
from Apps.Distribution.order.models import *

class Manufacturing_Order(models.Model):
    no_reg = models.CharField(verbose_name=_('Manufacturing Order'), max_length=25, editable=False) # no_reg = MO
    Production_Request = models.ForeignKey(SalesOrder, verbose_name=_('Permintaan Produksi'), limit_choices_to={'status': 3})
    Product = models.CharField(verbose_name=_('Produk'), max_length=35, help_text='Isi Dengan Nama Produk')
    ##Product = models.ForeignKey(Master_Product, verbose_name=_('Produk'))
    #Product_Quantity = models.IntegerField(verbose_name=_('Jumlah'), default=0, help_text='Jumlah Pesanan Produk')
    #Colour_Name = models.IntegerField(verbose_name=_('Jenis Warna'), choices=Warna_Produk, help_text='Pilihlah Warna Produk') # WARNA PRODUK
    #Label = models.IntegerField(verbose_name=_('Label'), choices=Label_Produk) # WARNA PRODUK
    #Category = models.IntegerField(verbose_name=_('Kategori'), choices=Kategori_Produk)
    Add_Date_Time = models.DateTimeField(verbose_name=_('Tanggal/Jam')) # tanggal masuk Manufacturing order dibuat
    #Add_Time = models.TimeField(verbose_name=_('Jam'))# jam masuk Manufacturing order dibuat

    class Meta:
        verbose_name="Manufacturing Order"
        verbose_name_plural="Manufacturing Order"

    def incstring(self):
        try:
            data = Manufacturing_Order.objects.all()
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
        return 'MO/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Manufacturing_Order, self).save()

    def ID(self):
        return ' %(no_reg)s | %(Product)s' % {'no_reg':self.no_reg,'Product':self.Product}
    ID.short_description='MO Number'


    def __unicode__(self):
        return ' %(no_reg)s | %(Product)s' % {'no_reg':self.no_reg,'Product':self.Product}
"""   
	def incstring(self):	
		try:
			data = Manufacturing_Order.objects.all()
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
		strnow = str(now)
		intyear = int(nowyear)
		
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		nol = 5 - self.inclen()
		if nol == 1: num = "0"
		elif nol == 2: num = "00"
		elif nol == 3: num = "000"
		elif nol == 4: num = "0000"
		number = num + self.incstring()
		return 'MO/%(unik)s/%(year)s/%(month)s' % {'unik' : number,
													'year' : intyear,
													'month' : strnow}
													
	def save(self):
		if self.no_reg == '':
			self.no_reg = self.no_req()
		else: self.no_reg = self.no_reg
		super(Manufacturing_Order, self).save()
	
	def __unicode__(self):
		return u'%s' % self.no_reg
		
	"""
# Create your models here.
