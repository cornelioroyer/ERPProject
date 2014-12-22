"""Develop By - Achmad Afiffudin N"""

from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import signals
from Apps.Asset.Penjualan.models import *
from Apps.Accounting.GeneralLedger.models import *
from Apps.Accounting.CashBank.models import *
from datetime import datetime, timedelta
from decimal import Decimal
from Apps.Accounting.CashBank.models import *
from Apps.Accounting.AccountReceivable.const import *
from Apps.Distribution.invoice.models import *
from Apps.Distribution.FromSales.models import *
from django.db.models import Q

class Detail_Sales_Account(models.Model):
    Invoice = models.ForeignKey(ReceivableInvoice, verbose_name=_('Faktur '))
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun '), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Detail Akun Penjualan')
        verbose_name_plural = _('Detail Akun Penjualan')
        ordering = ['-id']
        db_table = "FAAR | Akun Faktur"
        
    def __unicode__(self):
        return '%s' % self.Invoice.number

def create_detail_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry, Tr_Journal_Entry
    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Invoice.number)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Invoice.number, Account=instance.Account, Journal_Entry=j, Debit=instance.Invoice.total, Credit=0)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Invoice.number, Account=instance.Account, Debit=instance.Invoice.total, Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Invoice.number)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Invoice.number, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Invoice.total)
            else:
                 Detail_Journal_Entry.objects.create(Reference=instance.Invoice.number, Account=instance.Account, Debit=0, Credit=instance.Invoice.total)
signals.post_save.connect(create_detail_Journal, sender=Detail_Sales_Account, weak=False, dispatch_uid='create_detail_Journal')

PAYMENT_STATUS =  getattr(settings, 'PAYMENT_STATUS', ((1, ugettext('Credit')), (2, ugettext('Lunas'))))
class Tr_Sales_Receipt(models.Model):
    Invoice = models.OneToOneField(ReceivableInvoice, verbose_name=_('Faktur '))
    Total_Payment = models.DecimalField(_('Total yang harus dibayar '), max_digits=19, decimal_places=2, default=0)
    Total_Credit = models.DecimalField(_('Hutang Terbayar '), max_digits=19, decimal_places=2, default=0)
    Total_Residu = models.DecimalField(_('Sisa Hutang '), max_digits=19, decimal_places=2, default=0)
    Payment_Status = models.IntegerField(_('Status Pembayaran '), choices=PAYMENT_STATUS)

    class Meta:
        verbose_name = _('Pembayaran Penjualan')
        verbose_name_plural = _('Pembayaran Penjualan')
        ordering = ['-id']
        db_table = "FAAR | Info Pembayaran Faktur Penjualan"

    def __unicode__(self):
        return '%s' % self.Invoice.number

    def total_payment(self):
        total_payment = self.Invoice.total
        return total_payment
    total_payment.short_description = _('Total yang harus dibayar')

    def total_credit(self):
        total_credit = 0
        try:
            b = Tr_Sales_Payment.objects.filter(Invoice__id=self.id)
            for bs in b:
                total_credit += bs.Paid_Amount
        except:
            pass
            
        return total_credit
    total_credit.short_description = _('Hutang Terbayar')

    def total_residu(self):
        total_residu = 0
        total_residu = self.total_payment() - self.total_credit()
        return total_residu
    total_residu.short_description = _('Sisa Hutang')

    def payment_status(self):
        if self.total_residu() == 0:
            status = 'Lunas'
        elif self.total_credit() == 0:
            status = 'Belum Dibayar'
        else:
            status = 'Kredit'
        return status
    payment_status.short_description = _('Status Pembayaran')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.Total_Payment = self.total_payment()
        self.Total_Credit = self.total_credit()
        self.Total_Residu = self.total_residu()
        if self.Total_Residu > 0: self.Payment_Status = 1
        else: self.Payment_Status = 2
        super(Tr_Sales_Receipt, self).save()
        
PAYMENT_METHOD =  getattr(settings, 'PAYMENT_METHOD', ((1, ugettext('Cash')), (2, ugettext('Bank'))))
class Tr_Sales_Payment(models.Model):
    Payment_No = models.CharField(verbose_name=_('Nomor Pembayaran '), unique=True, null=True, blank=True, max_length=20)
    Invoice = models.ForeignKey(Tr_Sales_Receipt, verbose_name=_('Faktur '))
    Paid_Amount = models.DecimalField(_('Jumlah Pembayaran '), max_digits=19, decimal_places=2, default=0)
    Bank_Payment = models.ForeignKey(Ms_Bank, verbose_name=_('Pembayaran Bank'), blank=True, null=True, on_delete=models.SET_NULL,
    help_text='*) Jika Membayar Melalui Bank, Pilih Bank')
    Cash_Payment = models.ForeignKey(Ms_Cash, verbose_name=_('Pembayaran Kas'), blank=True, null=True, on_delete=models.SET_NULL,
    help_text='*) Jika Membayar Melalui Kas, Pilih Kas')
    Date = models.DateField(_('Tanggal Pembayaran'), default=datetime.now())
    Memo = models.TextField(verbose_name=_('Memo '), null=True, blank=True, max_length=50)
    Period = models.ForeignKey(Ms_Period, verbose_name=_('Periode '))
    Journal = models.ForeignKey(Ms_Journal, verbose_name=_('Tipe Jurnal '))
    Control = models.BooleanField(verbose_name=_('Persetujuan'), default=False, 
    help_text='*) Persetujuan Dilakukan Oleh Kasi Keuangan')
    
    class Meta:
        verbose_name = _('Pembayaran Penjualan')
        verbose_name_plural = _('Pembayaran Penjualan')
        ordering = ['-id']
        db_table = "FAAR | Pembayaran Penjualan"

    def __unicode__(self):
        return '%s' % self.Payment_No

    def incstring(self):
        try:
            data = Tr_Sales_Payment.objects.all().order_by('-Date')
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.Payment_No).split('/')
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
        return 'PBFAK/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
        
    def jurnal(self):
        a = Ms_Journal.objects.get(Type=4)
        if self.Bank_Payment is None and self.Cash_Payment is not None:
            a = Ms_Journal.objects.get(Type=4)
        elif self.Cash_Payment is None and self.Bank_Payment is not None:
            a = Ms_Journal.objects.get(Type=5)
        return a

    def status(self):
        ac = 0
        try:
            data = Detail_Sales_Payment_Account.objects.filter(Payment__id=self.id)
            ac = data.count()        
        except:
            pass
        if ac == 2:
            sts = 'Akun Terisi'
        else:
            sts = 'Akun Kosong'
        return sts

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.Payment_No is None:
            self.Payment_No = self.no_rek()
        else:
            self.Payment_No = self.Payment_No
        self.Period = self.period()
        self.Payment_Ref = self.Invoice.Invoice.number
        self.Journal = self.jurnal()
        super(Tr_Sales_Payment, self).save()

def create_journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    from Apps.Accounting.CashBank.models import Tr_Cash, Tr_Bank
    if instance.Control == True:
        n=0
        try:
            a = Tr_Journal_Entry.objects.filter(Reference=instance.Payment_No)
            n = a.count()
        except:
            pass
        if n == 0 :
            Tr_Journal_Entry.objects.create(Journal=instance.Journal, Journal_Period=instance.Period, Reference=instance.Payment_No, Memo=instance.Memo)
            if instance.Bank_Payment is None and instance.Cash_Payment is not None:
                Tr_Cash.objects.create(Reference=instance.Payment_No, Cash=instance.Cash_Payment, Debit=instance.Paid_Amount, Credit=0)
            else:
                Tr_Bank.objects.create(Reference=instance.Payment_No, Bank=instance.Bank_Payment, Debit=instance.Paid_Amount, Credit=0)

signals.post_save.connect(create_journal, sender=Tr_Sales_Payment, weak=False, dispatch_uid='create_Journal')

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    from Apps.Accounting.CashBank.models import Tr_Cash, Tr_Bank
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.Payment_No)
        n = a.count()
    except:
        pass
    if n == 1 :
        for x in a:
            b = x.Reference
            Tr_Journal_Entry.objects.filter(Reference=b).delete()
            Detail_Journal_Entry.objects.filter(Reference=b).delete()
            Tr_Cash.objects.filter(Reference=b).delete()
            Tr_Bank.objects.filter(Reference=b).delete()                                  
signals.post_delete.connect(delete_journal, sender=Tr_Sales_Payment, weak=False, dispatch_uid='delete_Journal')

class Detail_Sales_Payment_Account(models.Model):
    Payment = models.ForeignKey(Tr_Sales_Payment, verbose_name=_('Pembayaran '))
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun'), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Akun Pembayaran Penjualan')
        verbose_name_plural = _('Akun Pembayaran Penjualan')
        ordering = ['-id']
        db_table = "FAAR | Akun Pembayaran Penjualan"
        
    def __unicode__(self):
        return '%s' % self.Payment

def create_detail_journal_payment(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry, Tr_Journal_Entry
    from Apps.Accounting.CashBank.models import Tr_Bank, Tr_Cash
    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Payment.Payment_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Payment.Payment_No, Account=instance.Account, Journal_Entry=j,  Debit=instance.Payment.Paid_Amount, Credit=0)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Payment.Payment_No, Account=instance.Account, Debit=instance.Payment.Paid_Amount, Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Payment.Payment_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Payment.Payment_No, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Payment.Paid_Amount)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Payment.Payment_No, Account=instance.Account, Debit=0, Credit=instance.Payment.Paid_Amount)
signals.post_save.connect(create_detail_journal_payment, sender=Detail_Sales_Payment_Account, weak=False, dispatch_uid='create_detail_journal_payment')

class Detail_Return_Account(models.Model):
    Return = models.ForeignKey(Tr_Sales_Return, verbose_name=_('Retur '))
    #Return = models.CharField(verbose_name=_('Retur '), max_length=50)
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun '), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Akun Retur Penjualan')
        verbose_name_plural = _('Akun Retur Penjualan')
        ordering = ['-id']
        db_table = "FAAR | Retur Penjualan"

    def __unicode__(self):
        return '%s' % self.Return.Sales_Return_No

def create_detail_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Return.Sales_Return_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Return.Sales_Return_No, Account=instance.Account, Journal_Entry=j,  Debit=instance.Return.total(), Credit=0)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Return.Sales_Return_No, Account=instance.Account, Debit=instance.Return.total(), Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Return.Sales_Return_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Return.Sales_Return_No, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Return.total())
            else:
                 Detail_Journal_Entry.objects.create(Reference=instance.Return.Sales_Return_No, Account=instance.Account, Debit=0, Credit=instance.Return.total())
signals.post_save.connect(create_detail_Journal, sender=Detail_Return_Account, weak=False, dispatch_uid='create_detail_Journal')

class Sales_Return(Tr_Sales_Return):
    class Meta:
        proxy = True
        verbose_name = 'Akun Retur Penjualan'
        verbose_name_plural = 'Akun Retur Penjualan'

    def status(self):
        ac = 0
        try:
            data = Detail_Return_Account.objects.filter(Return__id=self.id)
            ac = data.count()        
        except:
            pass
        if ac == 2:
            sts = 'Akun Terisi'
        else:
            sts = 'Akun Kosong'
        return sts

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.Sales_Return_No)
        n = a.count()
    except:
        pass
    if n == 1:
        for x in a:
            b = x.Reference
            Tr_Journal_Entry.objects.get(Reference=b).delete()
            Detail_Journal_Entry.objects.filter(Reference=b).delete()
signals.post_delete.connect(delete_journal, sender=Sales_Return, weak=False, dispatch_uid='delete_Journal')

class Asset_Sale_Invoice(Tr_Asset_Sale_Invoice):
    class Meta:
        proxy = True
        verbose_name = 'Akun Penjualan Aset'
        verbose_name_plural = 'Akun Penjualan Aset'
    
    def status(self):
        ac = 0
        try:
            data = Detail_Asset_Sale_Account.objects.filter(Invoice__id=self.id)
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
    from Apps.Accounting.AccountPayable.models import Tr_Purchase_Pay
    d=0
    try:
        b = Tr_Asset_Sale_Receipt.objects.filter(Invoice=instance)
        d = b.count()
    except:
        pass
    if d == 0 :
        Tr_Asset_Sale_Receipt.objects.create(Invoice=instance)
    
signals.post_save.connect(create_payment, sender=Asset_Sale_Invoice, weak=False, dispatch_uid='create_payment')

def create_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry, Tr_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.no_reg)
        n = a.count()
    except:
        pass
    if n == 0 :
        Tr_Journal_Entry.objects.create(Journal=instance.journal, Journal_Period=instance.period, Reference=instance.no_reg, Memo=instance.info)
    else:
        Tr_Journal_Entry.objects.update(Journal=instance.journal, Journal_Period=instance.period, Reference=instance.no_reg, Memo=instance.info)

signals.post_save.connect(create_Journal, sender=Asset_Sale_Invoice, weak=False, dispatch_uid='create_detail_Journal')

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.no_reg)
        n = a.count()
    except:
        pass
    if n == 1:
        for x in a:
            b = x.Reference
            Tr_Journal_Entry.objects.get(Reference=b).delete()
            Detail_Journal_Entry.objects.filter(Reference=b).delete()
signals.post_delete.connect(delete_journal, sender=Asset_Sale_Invoice, weak=False, dispatch_uid='delete_Journal')

class Detail_Asset_Sale_Account(models.Model):
    Invoice = models.ForeignKey(Tr_Asset_Sale_Invoice, verbose_name=_('Faktur '))
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun '), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Akun Penjualan Aset')
        verbose_name_plural = _('Akun Penjualan Aset')
        ordering = ['-id']
        db_table = "FAAR | Akun Faktur Penjualan Aset"

    def __unicode__(self):
        return '%s' % self.Invoice.Invoice_No

def create_detail_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Invoice.Invoice_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Invoice.Invoice_No, Account=instance.Account, Journal_Entry=j,  Debit=instance.Invoice.total(), Credit=0)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Invoice.Invoice_No, Account=instance.Account, Debit=instance.Invoice.total(), Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Invoice.Invoice_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Invoice.Invoice_No, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Invoice.total())
            else:
                 Detail_Journal_Entry.objects.create(Reference=instance.Invoice.Invoice_No, Account=instance.Account, Debit=0, Credit=instance.Invoice.total())
signals.post_save.connect(create_detail_Journal, sender=Detail_Asset_Sale_Account, weak=False, dispatch_uid='create_detail_Journal')

PAYMENT_STATUS =  getattr(settings, 'PAYMENT_STATUS', ((1, ugettext('Credit')), (2, ugettext('Lunas'))))
class Tr_Asset_Sale_Receipt(models.Model):
    Invoice = models.OneToOneField(Tr_Asset_Sale_Invoice, verbose_name=_('Faktur '))
    Total_Payment = models.DecimalField(_('Total yang harus dibayar '), max_digits=19, decimal_places=2, default=0)
    Total_Credit = models.DecimalField(_('Hutang Terbayar '), max_digits=19, decimal_places=2, default=0)
    Total_Residu = models.DecimalField(_('Sisa Hutang '), max_digits=19, decimal_places=2, default=0)
    Payment_Status = models.IntegerField(_('Status Pembayaran '), choices=PAYMENT_STATUS)

    class Meta:
        verbose_name = _('Pembayaran Penjualan Aset')
        verbose_name_plural = _('Pembayaran Penjualan Aset')
        ordering = ['-id']
        db_table = "FAAR | Info Pembayaran Aset"

    def __unicode__(self):
        return u'%s' % self.Invoice

    def total_payment(self):
        total = self.Invoice.total()
        return total
    total_payment.short_description = _('Total yang harus dibayar')

    def total_credit(self):
        total_credit = 0
        try:
            b = Tr_Asset_Sale_Payment.objects.filter(Invoice__id=self.id)
            for bs in b:
                total_credit += bs.Paid_Amount
        except:
            pass
        return total_credit
    total_credit.short_description = _('Hutang Terbayar')

    def total_residu(self):
        total_residu = 0
        total_residu = self.total_payment() - self.total_credit()
        return total_residu
    total_residu.short_description = _('Sisa Hutang')

    def payment_status(self):
        if self.total_residu() == 0:
            status = 'Lunas'
        elif self.total_credit() == 0:
            status = 'Belum Dibayar'
        else:
            status = 'Kredit'
        return status
    payment_status.short_description = _('Status Pembayaran')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.Total_Payment = self.total_payment()
        self.Total_Credit = self.total_credit()
        self.Total_Residu = self.total_residu()
        if self.Total_Residu > 0: self.Payment_Status = 1
        else: self.Payment_Status = 2
        super(Tr_Asset_Sale_Receipt, self).save()
        
PAYMENT_METHOD =  getattr(settings, 'PAYMENT_METHOD', ((1, ugettext('Cash')), (2, ugettext('Bank'))))        
class Tr_Asset_Sale_Payment(models.Model):
    Payment_No = models.CharField(verbose_name=_('Nomor Pembayaran '), unique=True, null=True, blank=True, max_length=20)
    Invoice = models.ForeignKey(Tr_Asset_Sale_Receipt, verbose_name=_('Faktur '))
    Paid_Amount = models.DecimalField(_('Jumlah Pembayaran '), max_digits=19, decimal_places=2, default=0)
    Bank_Payment = models.ForeignKey(Ms_Bank, verbose_name=_('Pembayaran Bank'), blank=True, null=True, on_delete=models.SET_NULL)
    Cash_Payment = models.ForeignKey(Ms_Cash, verbose_name=_('Pembayaran Kas'), blank=True, null=True, on_delete=models.SET_NULL)
    Date = models.DateField(_('Tanggal Pembayaran'), default=datetime.now())
    Payment_Ref = models.CharField(verbose_name=_('Ref Faktur '), null=True, blank=True, max_length=20)
    Memo = models.TextField(verbose_name=_('Memo '), null=True, blank=True, max_length=50)
    Period = models.ForeignKey(Ms_Period, verbose_name=_('Periode '))
    Journal = models.ForeignKey(Ms_Journal, verbose_name=_('Tipe Jurnal '))
    Control = models.BooleanField(verbose_name=_('Persetujuan'), default=False, 
    help_text='*) Persetujuan Dilakukan Oleh Kasi Keuangan')

    class Meta:
        verbose_name = _('Pembayaran Penjualan Aset')
        verbose_name_plural = _('Pembayaran Penjualan Aset')
        ordering = ['-id']
        db_table = "FAAR | Pembayaran Penjualan Aset"

    def __unicode__(self):
        return '%s' % self.Payment_No

    def incstring(self):
        try:
            data = Tr_Asset_Sale_Payment.objects.all().order_by('Date')
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.Payment_No).split('/')
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
        return 'PASFAK/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def jurnal(self):
        a = Ms_Journal.objects.get(Type=4)
        if self.Bank_Payment is None and self.Cash_Payment is not None:
            a = Ms_Journal.objects.get(Type=4)
        elif self.Cash_Payment is None and self.Bank_Payment is not None:
            a = Ms_Journal.objects.get(Type=5)
        return a

    def status(self):
        ac = 0
        try:
            data = Detail_Asset_Sale_Payment_Account.objects.filter(Payment__id=self.id)
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.Payment_No is None:
            self.Payment_No = self.no_rek()
        else:
            self.Payment_No = self.Payment_No
        self.Period = self.period()    
        self.Payment_Ref = self.Invoice.Invoice.Invoice_No
        self.Journal = self.jurnal()
        super(Tr_Asset_Sale_Payment, self).save()

def create_journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    if instance.Control==True:
        n=0
        try:
            a = Tr_Journal_Entry.objects.filter(Reference=instance.Payment_No)
            n = a.count()
        except:
            pass
        if n == 0 :
            Tr_Journal_Entry.objects.create(Journal=instance.Journal, Journal_Period=instance.Period, Reference=instance.Payment_No, Memo=instance.Memo)
            if instance.Bank_Payment is None and instance.Cash_Payment is not None:
                Tr_Cash.objects.create(Reference=instance.Payment_No, Cash=instance.Cash_Payment, Debit=instance.Paid_Amount, Credit=0)  
            else:
                Tr_Bank.objects.create(Reference=instance.Payment_No, Bank=instance.Bank_Payment, Debit=instance.Paid_Amount, Credit=0)
signals.post_save.connect(create_journal, sender=Tr_Asset_Sale_Payment, weak=False, dispatch_uid='create_Journal')

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.Payment_No)
        n = a.count()
    except:
        pass
    if n == 1 :
        for x in a:
            b = x.Reference
            Tr_Journal_Entry.objects.filter(Reference=b).delete()
            Detail_Journal_Entry.objects.filter(Reference=b).delete()
            Tr_Cash.objects.filter(Reference=b).delete()
            Tr_Bank.objects.filter(Reference=b).delete()  
signals.post_delete.connect(delete_journal, sender=Tr_Asset_Sale_Payment, weak=False, dispatch_uid='delete_Journal')

class Detail_Asset_Sale_Payment_Account(models.Model):
    Payment = models.ForeignKey(Tr_Asset_Sale_Payment, verbose_name=_('Pembayaran '))
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun'), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Akun Pembayaran Aset')
        verbose_name_plural = _('Akun Pembayaran Aset')
        ordering = ['-id']
        db_table = "FAAR | Akun Pembahyaran Aset"

    def __unicode__(self):
        return '%s' % self.Payment

def create_detail_journal_payment(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry, Tr_Journal_Entry
    from Apps.Accounting.CashBank.models import Tr_Bank, Tr_Cash
    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Payment.Payment_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Payment.Payment_No, Account=instance.Account, Journal_Entry=j,  Debit=instance.Payment.Paid_Amount, Credit=0)     
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Payment.Payment_No, Account=instance.Account, Debit=instance.Payment.Paid_Amount, Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Payment.Payment_No)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Payment.Payment_No, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Payment.Paid_Amount)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Payment.Payment_No, Account=instance.Account, Debit=0, Credit=instance.Payment.Paid_Amount)
signals.post_save.connect(create_detail_journal_payment, sender=Detail_Asset_Sale_Payment_Account, weak=False, dispatch_uid='create_detail_journal_payment')

"""
#Pembayaran Penjualan
class Tr_Receipt(models.Model):
    From_Invoice = models.OneToOneField(Tr_Sales_Invoice, verbose_name=_('Nomor Faktur'))
    Payment_Status = models.IntegerField(_('Status Pembayaran'), choices=PAYMENT_STATUS_CHOICES)
    Total_Payment = models.DecimalField(_('Total yang harus dibayar'), max_digits=19, decimal_places=2, default=0)
    Total_Residu = models.DecimalField(_('Sisa Credit'), max_digits=19, decimal_places=2, default=0)
    Total_Credit = models.DecimalField(_('Total Credit'), max_digits=19, decimal_places=2, default=0)
    Total_Mulct = models.DecimalField(_('Total Denda'), max_digits=19, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('Penjualan')
        verbose_name_plural = _('Penjualan')
        ordering = ['From_Invoice']

    def __unicode__(self):
        return '%s' % (self.Payment_Status)

    def status(self):
        if (self.Total_Residu + self.Total_Mulct) > 0:
            status = 1
        elif self.Total_Residu == 0:
            status = 2
        return status

    def multct(self):
        if (self.From_Invoice.exp_day() > -30) and (self.From_Invoice.exp_day() < 0):
            self.Total_Mulct = (self.Total_Payment * (2)) / 50
        if (self.From_Invoice.exp_day() > -60) and (self.From_Invoice.exp_day() < -30):
            self.Total_Mulct = (self.Total_Payment * (4)) / 50
        if (self.From_Invoice.exp_day() > -90) and (self.From_Invoice.exp_day() < -60):
            self.Total_Mulct = (self.Total_Payment * (6)) / 50
        return self.Total_Mulct

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.Total_Payment = self.From_Invoice.total_payment
        self.Total_Residu = (self.Total_Payment) - (self.Total_Credit)
        self.Payment_Status = self.status()
        self.Total_Mulct = self.multct()
        super(Tr_Receipt, self).save()
"""
