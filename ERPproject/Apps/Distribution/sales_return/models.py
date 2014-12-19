from django.db import models
from Apps.Distribution.customer.models import Company
from Apps.Distribution.order.models import SalesOrder
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from Apps.Inventory.product.models import Category


RETURN = {('1', 'Pending'),('2', 'Accepted')}
TYPE = {('1', 'Kerusakan Saat Pengiriman'),('2', 'Produk Cacat/Rusak dalam pembuatan')}
PENANGANAN = {('1', 'Penggantian Total'),('2', 'Penggantian sebagian'), ('3', 'Dispose'), ('4', 'Tidak ada Penanganan')}
class Sales_Return(models.Model):
    so_reff = models.ForeignKey(SalesOrder, verbose_name=_('Referensi SO'))
    number = models.CharField(verbose_name=_('Nomer Return'), unique=True, null=True, blank=True, max_length=50,
                              editable=False)
    customer = models.ForeignKey(Company, verbose_name=_('Perusahaan '))
    date = models.DateField(verbose_name=_('Tanggal Return '), default=datetime.now())
    status = models.CharField(verbose_name=_('Status Return'), choices=RETURN, max_length=50)
    type_return = models.CharField(verbose_name=_('Tipe Return '), choices=TYPE, max_length=50)
    handling = models.CharField(verbose_name=_('Penanganan Return'), max_length=50, choices=PENANGANAN)

    def __unicode__(self):
        return self.number

    def incstring(self):
        try:
            data = Sales_Return.objects.all()
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.number).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rtn(self):
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
        return 'RTN/%(month)s/%(year)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.number is None:
            self.number = self.no_rtn()
        else:
            self.number = self.number
        super(Sales_Return, self).save()

COLOR = (('1', 'Flint'), ('2', 'Amber'), ('3', 'Green'))

class DetailReturn(models.Model):
    return_reff = models.ForeignKey(Sales_Return, verbose_name=_("Sales Return "))
    color = models.CharField(verbose_name=_('Warna Gelas '), max_length=50, choices=COLOR, help_text="*) Pilih warna gelas")
    category = models.ForeignKey(Category, verbose_name=_('Kategori '), blank=True, null=True)
    capacity = models.IntegerField(verbose_name=_('Kapasitas '),) #help_text='Kapasitas dalam mililiter (ml)')
    height = models.IntegerField(verbose_name=_('Tinggi '),) #help_text='Tinggi dalam milimeter (mm)')
    weight = models.IntegerField(verbose_name=_('Berat '),) #help_text='Berat dalam gram (gr)')
    diameter = models.IntegerField(verbose_name=_('Diameter '),)# help_text='Diameter dalam milimeter (mm)')
    image = models.ImageField(verbose_name=_('Design Botol '), upload_to='uploads/product/images', blank=True,
                              default='uploads/default.jpg', help_text='*) Desain botol, jika ada.')
    label = models.ImageField(verbose_name=_('Label Botol '), upload_to='uploads/product/label', blank=True,
                              default='uploads/default.jpg', help_text='*) Label botol, jika ada.')
    quantity = models.IntegerField(verbose_name=_('Kuantum '), default=0)