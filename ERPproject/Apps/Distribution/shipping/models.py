from django.db import models
from Apps.Distribution.customer.models import Company
from Apps.Distribution.master_sales.models import PaymentTerm, ShippingMethods, StaffPerson
from Apps.Accounting.CashBank.models import Ms_Currency, Ms_Tax
from library.const.order import PAYMENT_TYPE, SALES_TYPE, DELIVERY_STATUS_CHOICES
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from Apps.Distribution.invoice.models import ReceivableInvoice
class DeliveryOrder(models.Model):
    number = models.CharField(verbose_name=_('Nomer DO '), unique=True, null=True, blank=True, max_length=50,
                              editable=False)
    inv_reff = models.OneToOneField(ReceivableInvoice, verbose_name=_('Referensi SO '))
    customer = models.ForeignKey(Company, verbose_name=_('Nama Perusahaan '))
    staff_delivery = models.ForeignKey(StaffPerson, verbose_name=_('Staff Distribusi '), max_length=50, blank=True, null=True,
                                       limit_choices_to={'user__is_staff': True})
    status = models.IntegerField(verbose_name=_('Status Pengiriman '), max_length=50, choices=DELIVERY_STATUS_CHOICES, default=1)
    date = models.DateField(verbose_name=_('Tanggal DO '), default=datetime.now())
    payment_term = models.ForeignKey(PaymentTerm, verbose_name=_('Jangka Pembayaran '), default=2)
    currency = models.ForeignKey(Ms_Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    tax = models.ForeignKey(Ms_Tax, verbose_name=_('Jenis Pajak '), default=1)
    shipping_methods = models.ForeignKey(ShippingMethods, verbose_name=_('Perlakuan '), default=1)
    ship_date = models.DateField(verbose_name=_('Tanggal Pengiriman '), default=datetime.now())
    ship_address = models.TextField(verbose_name=_("Alamat Pengiriman "), blank=True)
    payment_type = models.IntegerField(verbose_name=_('Jenis Pembayaran '), max_length=50,
                                       choices=PAYMENT_TYPE)
    po_reference = models.CharField(verbose_name=_('Referensi PO '), max_length=50, blank=True)
    sales_type = models.IntegerField(verbose_name=_("Tipe Penjualan "), max_length=50, choices=SALES_TYPE, blank=True, null=True)
    term_service = models.TextField(verbose_name=_("Term of Service "), blank=True)
    quotation = models.TextField(verbose_name=_("Permintaan Khusus "), blank=True)
    total = models.DecimalField(verbose_name=_("Total Pembayaran"), decimal_places=2, max_digits=20, default=0)

    class Meta:
        verbose_name = "Delivery Order"
        verbose_name_plural = "Delivery Order"
        ordering = ["-date"]

    def __unicode__(self):
        return '%(no)s - %(customer)s' % {'no': self.number, 'customer': self.customer}

    def incstring(self):
        try:
            data = DeliveryOrder.objects.all()
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

    def no_do(self):
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
        return 'DO/%(month)s/%(year)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.number is None:
            self.number = self.no_do()
        else:
            self.number = self.number
        super(DeliveryOrder, self).save()
