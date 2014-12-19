from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from Apps.Distribution.order.models import SalesOrder
from Apps.Distribution.customer.models import Company
from Apps.Distribution.master_sales.models import PaymentTerm, ShippingMethods, StaffPerson
from Apps.Accounting.CashBank.models import Ms_Period, Ms_Journal, Ms_Currency, Ms_Tax
from library.const.order import PAYMENT_TYPE, SALES_TYPE, INVOICE_STATUS_CHOICES

def collect(request):
    return request.user

class ReceivableInvoice(models.Model):
    number = models.CharField(verbose_name=_('Nomer Invoice '), unique=True, null=True, blank=True, max_length=50, editable=False)
    so_reff = models.OneToOneField(SalesOrder, verbose_name=_('Referensi SO '))
    customer = models.ForeignKey(Company, verbose_name=_('Nama Perusahaan '))
    period = models.ForeignKey(Ms_Period, verbose_name=_("Periode "), editable=False)
    journal = models.ForeignKey(Ms_Journal, verbose_name=_("Journal "), editable=False)
    sales_person = models.ForeignKey(StaffPerson, verbose_name=_('Sales Staff '), max_length=50, blank=True, null=True,
                                     limit_choices_to={'user__is_staff': True}, editable=False)
    status = models.IntegerField(verbose_name=_('Status Order '), max_length=50, choices=INVOICE_STATUS_CHOICES, default=1)
    date = models.DateField(verbose_name=_('Tanggal Faktur '), default=datetime.now())
    payment_term = models.ForeignKey(PaymentTerm, verbose_name=_('Jangka Pembayaran '), default=2)
    currency = models.ForeignKey(Ms_Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    tax = models.ForeignKey(Ms_Tax, verbose_name=_('Jenis Pajak '), default=1)
    po_reference = models.CharField(verbose_name=_('Referensi PO '), max_length=50, blank=True,
                                    help_text='*) Isi dengan Referensi PO dari perusahaan customer ')
    shipping_methods = models.ForeignKey(ShippingMethods, verbose_name=_('Perlakuan '), default=1)
    ship_address = models.TextField(verbose_name=_("Alamat Pengiriman "), blank=True)
    payment_type = models.IntegerField(verbose_name=_('Jenis Pembayaran '), max_length=50,
                                       choices=PAYMENT_TYPE)
    term_service = models.TextField(verbose_name=_("Term of Service "), blank=True)
    quotation = models.TextField(verbose_name=_("Permintaan Khusus "), blank=True)
    sales_type = models.IntegerField(verbose_name=_("Tipe Penjualan "), max_length=50, choices=SALES_TYPE, blank=True, null=True)
    total = models.DecimalField(verbose_name=_("Total Pembayaran"), decimal_places=2, max_digits=20, default=0)

    class Meta:
        verbose_name = "Faktur Penjualan"
        verbose_name_plural = "Faktur Penjualan"
        ordering = ["-date"]
        db_table = "Distribusi | Faktur Penjualan"

    def __unicode__(self):
        return '%s' % self.number
    
    def incstring(self):
        try:
            data = ReceivableInvoice.objects.all()
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

    def receivable_invoice_id(self):
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
        return 'INV/%(month)s/%(year)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def period(self):
        today = datetime.now().date()
        a = 0
        try:
            per = Ms_Period.objects.filter(Start_Period__lte=today, End_Period__gte=today)
            a = per.count()
        except:
            pass
        if a == 1:
            for x in per:
                b = x.Code
                c = Ms_Period.objects.get(Code=b)
        else:
            c = self.Period
        return c

    def journal(self):
        a = Ms_Journal.objects.get(Type=1)
        return a

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.number is None:
            self.number = self.receivable_invoice_id()
        else:
            self.number = self.number
        self.period = self.period()
        self.journal = self.journal()
        super(ReceivableInvoice, self).save()

COLOR = (('1', 'Flint'), ('2', 'Amber'), ('3', 'Green'))
from Apps.Inventory.product.models import Category
from django.conf import settings
from PIL import Image


class DetailFaktur(models.Model):
    so_reff = models.OneToOneField(ReceivableInvoice, verbose_name=_("Referensi SO "), blank=True, null=True)
    name = models.CharField(verbose_name=_('Nama Item '), blank=True, default="Botol", max_length=50)
    color = models.CharField(verbose_name=_('Warna Gelas '), max_length=50, choices=COLOR, help_text="*) Pilih warna gelas")
    category = models.ForeignKey(Category, verbose_name=_('Jenis Botol '), blank=True, null=True, related_name="Kategori di Faktur")
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
        verbose_name = 'Detail Faktur'
        verbose_name_plural = 'Detail Faktur'
        ordering = ['name']
        db_table = "Distribusi | Detail Faktur"

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
        super(DetailFaktur, self).save()
        image = Image.open(self.image)
        (width, height) = image.size
        size = (125, 150)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)

        if not self.label:
            return

        super(DetailFaktur, self).save()
        label = Image.open(self.label)
        (width, height) = label.size
        size = (125, 150)
        label = label.resize(size, Image.ANTIALIAS)
        label.save(self.label.path)

class Sales_Invoice(ReceivableInvoice):
    class Meta:
        proxy = True
        verbose_name = 'Akun Faktur Penjualan'
        verbose_name_plural = 'Akun Faktur Penjualan'

    def sts(self):
        from Apps.Accounting.AccountReceivable.models import Detail_Sales_Account
        ac = 0
        try:
            data = Detail_Sales_Account.objects.filter(Invoice__id=self.id)
            ac = data.count()
        except:
            pass
        if ac == 2:
            sts = 'Akun Terisi'
        elif ac == 1:
            sts = 'Akun Tidak Lengkap'
        else:
            sts = 'Akun Kosong'
        return sts

def create_payment(sender, created, instance, **kwargs):
    from Apps.Accounting.AccountReceivable.models import Tr_Sales_Receipt
    d=0
    try:
        b = Tr_Sales_Receipt.objects.filter(Invoice=instance)
        d = b.count()
        if d == 0 :
            Tr_Sales_Receipt.objects.create(Invoice=instance)
    except:
        pass

signals.post_save.connect(create_payment, sender=Sales_Invoice, weak=False, dispatch_uid='create_payment')

def create_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry, Tr_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.number)
        n = a.count()
        if n == 0 :
            Tr_Journal_Entry.objects.create(Journal=instance.journal, Journal_Period=instance.period, Reference=instance.number, Memo=instance.term_service)
    except:
        pass

signals.post_save.connect(create_Journal, sender=Sales_Invoice, weak=False, dispatch_uid='create_Journal')

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.number)
        n = a.count()
        if n == 1:
            for x in a:
                b = x.Reference
                Tr_Journal_Entry.objects.get(Reference=b).delete()
                Detail_Journal_Entry.objects.filter(Reference=b).delete()
    except:
        pass
signals.post_delete.connect(delete_journal, sender=Sales_Invoice, weak=False, dispatch_uid='delete_Journal')
