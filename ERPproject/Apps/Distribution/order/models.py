from Apps.Distribution.master_sales.models import *
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from Apps.Distribution.customer.models import Company
#from Apps.Accounting.CashBank.models import Ms_Currency, Ms_Tax
from library.const.order import PAYMENT_TYPE, SO_STATUS_CHOICES, SALES_TYPE
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from PIL import Image
from Apps.Inventory.product.models import Category
from decimal import *
from datetime import datetime

COLOR = (('1', 'Flint'), ('2', 'Amber'), ('3', 'Green'))

class SalesOrder(models.Model):
    number = models.CharField(verbose_name=_('Nomer SO '), unique=True, null=True, blank=True, max_length=50,
                              editable=False)
    customer = models.ForeignKey(Company, verbose_name=_('Nama Perusahaan '))
    sales_person = models.ForeignKey(StaffPerson, verbose_name=_('Staf Penjualan '), max_length=50, blank=True, null=True)
    status = models.IntegerField(verbose_name=_('Status Order '), max_length=50, choices=SO_STATUS_CHOICES, default=1)
    date = models.DateField(verbose_name=_('Tanggal Permintaan '), default=datetime.now())
    payment_term = models.ForeignKey(PaymentTerm, verbose_name=_('Jangka Pembayaran '), default=2)
    #currency = models.ForeignKey(Ms_Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    #tax = models.ForeignKey(Ms_Tax, verbose_name=_('Jenis Pajak '), default=1)
    currency = models.ForeignKey(Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    tax = models.ForeignKey(Tax, verbose_name=_('Jenis Pajak '), default=1)
    po_reference = models.CharField(verbose_name=_('Referensi PO '), max_length=50, blank=True,
                                    help_text='*) Referensi PO dari perusahaan customer ')
    shipping_methods = models.ForeignKey(ShippingMethods, verbose_name=_('Perlakuan '), default=1)
    shipping_address = models.TextField(verbose_name=_('Alamat Pengiriman '), blank=True)
    payment_type = models.IntegerField(verbose_name=_('Jenis Pembayaran '), max_length=50,
                                       choices=PAYMENT_TYPE, default=2)
    sales_type = models.IntegerField(verbose_name=_("Tipe Penjualan "), max_length=50, choices=SALES_TYPE,
                                     blank=True, null=True, default=1)
    term_service = models.TextField(verbose_name=_("Term of Service "), blank=True)
    quotation = models.TextField(verbose_name=_("Permintaan Khusus "), blank=True)
    total = models.DecimalField(verbose_name=_("Total Pembayaran "), null=True, decimal_places=2, max_digits=20, default=0)

    class Meta:
        verbose_name = "Order Penjualan"
        verbose_name_plural = "Order Penjualan"
        ordering = ["-date"]
        db_table = "Distribusi | Order Penjualan"

    def __unicode__(self):
        return '%(no)s - %(customer)s' % {'no': self.number, 'customer': self.customer}

    def subtotal(self):
        subtotal = Decimal(0)
        try:
            allitem = OrderItem.objects.filter(so_reff__id=self.id)
            for item in allitem:
                subtotal += item.amount()
        except:
            pass
        return subtotal
    subtotal.short_description = _('Subtotal')

    @property
    def total_tax(self):
        if self.tax:
            total_tax = (self.subtotal() * self.tax.percentage) / 50
        else:
            total_tax = Decimal(0)
        return total_tax.quantize(Decimal('0.01'), ROUND_HALF_UP)

    def total_price(self):
        try:
            if not self.tax:
                return self.subtotal()
            else:
                return self.subtotal() + self.total_tax
        except:
            ObjectDoesNotExist
    total_price.short_description = _('Total ')

    def display_price(self):
        return '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': intcomma(self.total_price()),
                                               'back': self.currency.post_symbol}
    display_price.short_description = _('Total Bayar')

    def incstring(self):
        try:
            data = SalesOrder.objects.all()
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

    def no_so(self):
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
        return 'SO/%(month)s/%(year)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        self.total = self.total_price()
        if self.number is None:
            self.number = self.no_so()
        else:
            self.number = self.number
        super(SalesOrder, self).save()

    def print_pdf(self):
        img = '<img src="/media/static/staticproc/images/print.png" width="20%"/>'
        link = '<a href="/print_so/%(id)s/" target="blank">%(gbr)s Cetak</a>' % {'id': self.id, 'gbr':img}
        return link
    print_pdf.allow_tags = True
    print_pdf.short_description = 'Print SO'


class RequestOrder(SalesOrder):
    class Meta:
        proxy = True
        verbose_name_plural = _('Order Permintaan')
        verbose_name = _('Order Permintaan')
        ordering = ["-date"]
        db_table = "Distribusi | Order Permintaan"


class QuoteOrder(SalesOrder):
    class Meta:
        proxy = True
        verbose_name_plural = _('Order Penawaran')
        verbose_name = _('Order Penawaran')
        ordering = ["-date"]
        db_table = "Distribusi | Order Penawaran"


class OrderItem(models.Model):
    so_reff = models.OneToOneField(SalesOrder, verbose_name=_("Referensi SO "), blank=True, null=True)
    name = models.CharField(verbose_name=_('Nama Item '), blank=True, default="Botol", max_length=50)
    color = models.CharField(verbose_name=_('Warna Gelas '), max_length=50, choices=COLOR, help_text="*) Pilih warna gelas")
    category = models.ForeignKey(Category, verbose_name=_('Jenis Botol '), blank=True, null=True)
    capacity = models.IntegerField(verbose_name=_('Kapasitas '),) #help_text='Kapasitas dalam mililiter (ml)')
    height = models.IntegerField(verbose_name=_('Tinggi '),) #help_text='Tinggi dalam milimeter (mm)')
    weight = models.IntegerField(verbose_name=_('Berat '),) #help_text='Berat dalam gram (gr)')
    diameter = models.IntegerField(verbose_name=_('Diameter '),)# help_text='Diameter dalam milimeter (mm)')
    image = models.ImageField(verbose_name=_('Design Botol '), upload_to='uploads/product/images', blank=True,
                              default='uploads/default.jpg', help_text='*) Desain botol, jika ada.')
    label = models.ImageField(verbose_name=_('Label Botol '), upload_to='uploads/product/label', blank=True,
                              default='uploads/default.jpg', help_text='*) Label botol, jika ada.')
    price = models.DecimalField(verbose_name=_ ('Harga Produk '), max_digits=20, decimal_places=2, default=0)
    quantity = models.IntegerField(verbose_name=_('Jumlah '), default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Detail Item'
        verbose_name_plural = 'Detail Item'
        ordering = ['name']
        db_table = "Distribusi | Detail Order"

    def amount(self):
        return self.price * self.quantity
    amount.short_description = _('Harga Produk ')

    def display_image(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="90"/>' % (settings.MEDIA_URL, self.image)

    def display_label(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="90"/>' % (settings.MEDIA_URL, self.label)

    def save(self, force_insert=True, force_update=True, using=None,
             update_fields=None):
        if not self.image:
            return
        super(OrderItem, self).save()
        image = Image.open(self.image)
        (width, height) = image.size
        size = (125, 150)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)

        if not self.label:
            return

        super(OrderItem, self).save()
        label = Image.open(self.label)
        (width, height) = label.size
        size = (125, 150)
        label = label.resize(size, Image.ANTIALIAS)
        label.save(self.label.path)
