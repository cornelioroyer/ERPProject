from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import *
from datetime import datetime
from django.db.models.signals import post_save
#from mptt.fields import TreeForeignKey
#from mptt.models import MPTTModel

class Ms_asset(models.Model):
    no_reg = models.CharField(verbose_name='Plat Number ', max_length=25, editable=False)
    asset_name = models.CharField(verbose_name=_('Nama Asset '),max_length=50)
    type =  models.ForeignKey(Asset_type, verbose_name=('Tipe Aset '))
    end_warranty = models.DateField(verbose_name=('Masa Garansi'), blank=True, null=True)
    #parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    #order = models.IntegerField()
    location  = models.ForeignKey('self', verbose_name=('Lokasi'),blank=True,null=True , help_text=' penempatan asset')
    department =  models.ForeignKey(Department, verbose_name=('Kepemilikan Departement '))
    #salvage = models.DecimalField(verbose_name=_('Nilai Residu'), max_digits=20, decimal_places=2)
    price = models.DecimalField(verbose_name=('Harga Beli'), max_digits=20, decimal_places=2)
    life_time = models.IntegerField(verbose_name=('Estimasi Pemakaian (Thn)'), help_text=' kurun waktu satu tahun')
    salvage = models.DecimalField(verbose_name=('Harga Sisa'), max_digits=20, decimal_places=2, help_text=' nilai penyelamatan aset')
    condition = models.IntegerField(verbose_name=('Kondisi'), choices=Choice_kondisi, default=1)
    #by = models.IntegerField(verbose_name=('Per'),choices=per_choices)
    #persent = models.CharField(verbose_name=('Persen'),max_length=2, help_text='% tiap waktu yg ditentukan')
    add_date = models.DateField(verbose_name=('tgl masuk'))
    freq_m = models.IntegerField(verbose_name=('Frekuensi Pemeliharaan'), choices=Freq_pemeliharaan, default=3)
    status_loan = models.IntegerField(verbose_name=('Status Peminjaman'),choices=Choice_peminjaman, default=1, editable=False)
    usage_status = models.IntegerField(verbose_name=('Status Penggunaan'),choices=Usage_choice, default=1,editable=False)
    maintenance_status = models.IntegerField(verbose_name=('Status Maintenance'),choices=status_maintenance, default=1)
    plan_month = models.CharField(max_length=6, editable=False)

    def jadwal_maintenance(self):
        from Apps.Asset.Maintenance.models import Data_maintenance_asset
        n = 0
        try:
            d = Data_maintenance_asset.objects.filter(asset__asset_name=self.asset_name)
            n = d.count()
        except:
            pass
        if n > 0:
            for ds in d:
                masuk = ds.header_maintenance.rm_add_date.strftime("%m")
        else:
            masuk = self.add_date.strftime("%m")
        bln_m = int(masuk) + int(self.freq_m)

        if bln_m > 12:
            bln_m -= 12

        str_bln = 'Bulan '
        if bln_m == 1: str_bln +='Januari'
        elif bln_m == 2: str_bln +='Februari'
        elif bln_m == 3: str_bln +='Maret'
        elif bln_m == 4: str_bln +='April'
        elif bln_m == 5: str_bln +='Mei'
        elif bln_m == 6: str_bln +='Juni'
        elif bln_m == 7: str_bln +='Juli'
        elif bln_m == 8: str_bln +='Agustus'
        elif bln_m == 9: str_bln +='September'
        elif bln_m == 10: str_bln +='Oktober'
        elif bln_m == 11: str_bln +='November'
        elif bln_m == 12: str_bln +='Desember'

        now = datetime.now().strftime("%m")
        now_s = int(now)
        if bln_m == now_s:
            str_bln = '<font color="red"><b>Warning maintenance</b></font>'

        return '%(x)s' % {'x':str_bln}
    jadwal_maintenance.allow_tags = True

    def tot(self):
        hrg = self.price
        a = datetime.now().strftime("%Y")
        p = datetime.now().strftime("%m")
        b = self.add_date.strftime("%Y")
        q = self.add_date.strftime("%m")

        sel_thn = int(a) - int(b)
        if int(p) >= int(q):
            if sel_thn >= 1 :
                sel_thn = int(a) - int(b)
        else:
            if sel_thn > 1 :
                sel_thn = (int(a)-1) - int(b)
            elif sel_thn == 1:
                sel_thn = 0


        d = self.price - int(self.salvage)

        r = d / self.life_time

        hasil = sel_thn * r

        return hrg - hasil

    def nilai_sisa_asset(self):
        return 'Rp. %(x)s' % {'x':self.tot()}

    def nilai_penyusutan(self):
        d = self.price - int(self.salvage)
        r = d / self.life_time
        return r

    class Meta:
        verbose_name_plural="Master Asset "
        verbose_name="Master_Asset"
        ''' Untuk Nomer Plat Asset
         ======================='''
    def incstring(self):
        try:
            data = Ms_asset.objects.all()
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
        return 'ITEM/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def now(self):
        n = datetime.now().strftime("%m %Y")
        return n

    def cobax(self):
        from Apps.Accounting.GeneralLedger.models import depresiation_record
        g = 0
        try:
            f = depresiation_record.objects.filter(ref_asset__id=self.id)
            g = f.count()
        except:
            pass
        h = g + 1
        month = self.add_date.strftime("%m")
        a = self.add_date.strftime("%Y")
        b = int(a) + h
        year = str(b)
        d = '%(month)s %(year)s' % {'month': month,'year': year}
        return d

    def cobaxx(self):
        from Apps.Accounting.GeneralLedger.models import depresiation_record
        g = 0
        try:
            f = depresiation_record.objects.filter(ref_asset__id=self.id)
            g = f.count()
        except:
            pass
        h = g + 1
        day = self.add_date.strftime("%d")
        month = self.add_date.strftime("%m")
        a = self.add_date.strftime("%Y")
        b = int(a) + h
        year = str(b)
        d = '%(day)s/%(month)s/%(year)s' % {'day': day,'month': month,'year': year}
        return d

    def count(self):
        from Apps.Accounting.GeneralLedger.models import depresiation_record
        g = 0
        try:
            f = depresiation_record.objects.filter(ref_asset__id=self.id)
            g = f.count()
        except:
            pass
        return g

    def coba(self):
        from Apps.Accounting.GeneralLedger.models import depresiation_record
        g = 0
        try:
            f = depresiation_record.objects.filter(ref_asset__id=self.id, dep_no=self.count())
            g = f.count()
        except:
            pass
        if self.now() == self.cobax() and g == 0:
            str_bln='<font color="red"><b>waktu laporan penyusutan</b></font>'
            return '%(x)s' % {'x':str_bln}
        else:
            return 'Laporan Selanjutnya %(name)s' %{'name':self.cobaxx()}
    coba.allow_tags=True
    coba.short_description=_('Pelaporan Penyusutan')

    def plan_mon(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)

        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}

        return '%(year)s%(month)s' % {'year':intyear, 'month':strnow}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        if self.plan_month == '':
            self.plan_month = self.plan_mon()
        else: self.plan_month = self.plan_month
        super(Ms_asset, self).save()
        #Ms_asset.objects.rebuild()

        #def get_absolute_url(self):
        #	return reverse('Apps.Asset.Master.views.lock_rkb', args=[self.id])

    def ID(self):
        return ' %(no_reg)s | %(asset_name)s' % {'no_reg':self.no_reg,'asset_name':self.asset_name}
    ID.short_description='Plat Number'


    def __unicode__(self):
        return '%(no_reg)s | %(asset_name)s' %{'no_reg':self.no_reg,'asset_name':self.asset_name}

def create_dep(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import depresiation_record
    b = 0
    try:
        a = depresiation_record.objects.filter(ref_asset=instance)
        b = a.count()
    except:
        pass
    now = datetime.now().strftime("%m %Y")
    month = instance.add_date.strftime("%m")
    y = instance.add_date.strftime("%Y")
    c = b + 1
    i = int(y) + c
    year = str(i)
    d = '%(month)s %(year)s' % {'month': month,'year': year}
    g = 0
    try:
        f = depresiation_record.objects.filter(ref_asset__id=self.id, dep_no=self.count())
        g = f.count()
    except:
        pass
    if now == d and g==0:
        depresiation_record.objects.create(ref_asset=instance,dep_no=c,dep_value=instance.tot())
signals.post_save.connect(create_dep, sender=Ms_asset, weak=False, dispatch_uid='create_dep')

def delete_asset(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import depresiation_record
    depresiation_record.objects.filter(ref_asset=instance).delete()
signals.post_delete.connect(delete_asset, sender=Ms_asset, weak=False, dispatch_uid='delete_asset')

#class MPTTMeta:
#    order_insertion_by = ['order']


class Historical_asset(models.Model):
    no_reg = models.CharField(verbose_name='Plat Number ', max_length=25, editable=False)
    asset_name = models.CharField(verbose_name=_('Nama Asset '),max_length=50)
    type =  models.ForeignKey(Asset_type, verbose_name=('Tipe Aset '))
    department =  models.ForeignKey(Department, verbose_name=('Kepemilikan Departement '))
    add_date = models.DateField(verbose_name=('tgl masuk'))
    disposal_date = models.DateTimeField(verbose_name=_('waktu penghapusan'),auto_now_add=True)

    class Meta:
        verbose_name_plural="Riwayat Asset "
        verbose_name="Riwayat_Asset"

    def __unicode__(self):
        return '%s' % self.id

"""
class Category(MPTTModel):
	name = models.Charfield(max_length=64)
	parent = TreeForeignKey ('self', null= True , blank=True , related_name='children')
	order = models.PositiveInteger()
	
	class MPTTMeta:
		order_insertion_by = ['order']

	def save(self, *args, **kwargs):
		super(Category, self).save(*args, **kwargs)
		Category.objects.rebuild()
	def __unicode__(self):
		return self.name
"""

 

