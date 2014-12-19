from django.db import models
from tinymce.models import HTMLField
from Apps.Procurement.vendor.const.const import *
from datetime import datetime
from Apps.Procurement.vendor.models import Ms_Vendor
from Apps.Procurement.property.models import Set_Of_Delay
from Apps.Accounting.GeneralLedger.models import *

class Purchase_Order(models.Model):
    no_reg = models.CharField(verbose_name='No Reg', max_length=25, blank=True, null=True, editable=False)
    vendor = models.ForeignKey(Ms_Vendor, verbose_name='Nama Vendor')
    po_add_date = models.DateTimeField(verbose_name='Tgl Buat', auto_now_add=True)
    po_month = models.CharField(verbose_name='Bulan', max_length=6, editable=False)
    ship_to = HTMLField(verbose_name='Dikirim ke Alamat', blank=True)
    po_status = models.IntegerField(max_length=1, choices=PO_STATUS_CHOICES)
    delay_fine = models.IntegerField(verbose_name='Denda', max_length=3, help_text='% Denda yg akan di bebankan ketika keterlambatan kedatangan barang')
    set_of_delay = models.ForeignKey(Set_Of_Delay, verbose_name='Satuan Keterlambatan per')
    po_agreement = HTMLField(verbose_name='Perjanjian', blank=True)
    goods_receipt_plan = models.DateField(verbose_name='Tgl Penerimaan', blank=True, null=True, help_text='Tgl rencana penerimaan barang')
    po_date_sent = models.DateTimeField(verbose_name='Tgl Kirim PO', blank=True, null=True, editable=False)
    Period = models.ForeignKey(Ms_Period, verbose_name='Periode ', editable=False)
    Journal = models.ForeignKey(Ms_Journal, verbose_name='Tipe Jurnal ', editable=False)

    class Meta:
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Order'
        ordering = ['id']

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
            data = Purchase_Order.objects.filter(po_month=bln).order_by('po_add_date')
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

    def pur_m(self):
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

    def total_(self):
        total = 0
        from Apps.Procurement.internal.models import Data_Purchase_Request, Data_Rush_Order
        try:
            data = Data_Purchase_Request.objects.filter(no_po__id=self.id)
            for d in data:
                total += d.request_total_price
        except:
            pass

        try:
            data2 = Data_Rush_Order.objects.filter(no_po__id=self.id)
            for d in data2:
                total += d.ro_total_price
        except:
            pass
        return total
    total_.short_description = 'Total Pengeluaran'

    def ppn10(self):
        ppn = total = 0
        ppn = (self.total_() / 100) * 10
        return ppn
    ppn10.short_description = 'Pajak'

    def total_expenditure(self):
        total = 0
        total = self.total_() + self.ppn10()
        return total
    total_expenditure.short_description = '+PPN 10%'

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_po(self):
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
        return 'PO/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
                                                   'month' : strnow,
                                                   'unik' : number}

    def ship_tox(self):
        return '%s' % self.ship_to
    ship_tox.allow_tags = True
    ship_tox.short_description = 'Dikirim ke Alamat'

    def ship_to_pdf(self):
        get = self.ship_to[3:-4]
        #plus = '<p style="font-size:70%">'
        #plus = plus + get
        return '%s' % get

    def po_agreementx(self):
        return '%s' % self.po_agreement
    po_agreementx.allow_tags = True
    po_agreementx.short_description = 'Perjanjian'

    def print_pdf(self):
        img = '<img src="/media/static/staticproc/images/print.png" width="20%"/>'
        link = '<a href="/print_po_admin/%(id)s/" target="blank">%(gbr)s Cetak</a>' % {'id':self.id, 'gbr':img}
        return link
    print_pdf.allow_tags = True
    print_pdf.short_description = 'Print PO'

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
        a = 0
        try:
            jur = Ms_Journal.objects.filter(Type=2)
            a = jur.count()
        except:
            pass
        if a == 1:
            for x in jur:
                b = x.Code
                c = Ms_Journal.objects.get(Code=b)
        else:
            c = self.Journal
        return c

    def save(self, force_insert=False, force_update=False, using=None):
        if self.no_reg is None:
            self.no_reg = self.no_po()
        else: self.no_reg = self.no_reg
        self.Period = self.period()
        self.Journal = self.journal()
        if self.po_status == 21:
            now = datetime.now()
            if self.po_month == '':
                self.po_month = self.pur_m()
            else: self.po_month = self.po_month
            if self.po_date_sent is None:
                self.po_date_sent = now
            else: self.po_date_sent = self.po_date_sent
        super(Purchase_Order, self).save()

    def __unicode__(self):
        strid = '%(no_reg)s | %(ven)s' % {'no_reg':self.no_reg,'ven':self.vendor.vendor_name}
        return strid

class Contract(models.Model):
    no_contract = models.CharField(verbose_name='No Kontrak', max_length=25, blank=True, null=True, editable=False)
    vendor = models.ForeignKey(Ms_Vendor, verbose_name='Nama Vendor')
    no_po = models.ForeignKey(Purchase_Order, verbose_name='PO Reference')
    con_add_date = models.DateTimeField(verbose_name='Tgl Buat', auto_now_add=True)
    con_month = models.CharField(verbose_name='Bulan', max_length=6, editable=False)
    start_date = models.DateField(verbose_name='Tgl Mulai')
    end_date = models.DateField(verbose_name='Tgl Selesai')

    class Meta:
        verbose_name = 'Kontrak'
        verbose_name_plural = 'Kontrak'
        ordering = ['id']

    def status_int(self):
        now = datetime.now().utcnow().date()
        end_date = self.end_date
        status = 1
        left = end_date-now

        if left.days > 0:
            status = 2
        return status

    def status(self):
        int_stat = self.status_int()
        str_stat = ''
        if int_stat == 1:
            str_stat = 'Selesai'
        else: str_stat = 'Kontrak aktif'
        return str_stat

    def con_m(self):
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
            data = Contract.objects.filter(con_month=bln).order_by('con_add_date')
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

    def no_con(self):
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
        return 'CONTRACT/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
                                                         'month' : strnow,
                                                         'unik' : number}

    def save(self, force_insert=False, force_update=False, using=None):
        if self.no_contract is None:
            self.no_contract = self.no_con()
        else: self.no_contract = self.no_contract
        if self.con_month == '':
            self.con_month = self.con_m()
        else: self.con_month = self.con_month
        super(Contract, self).save()

class Payable_PO(Purchase_Order):
    class Meta:
        proxy = True
        verbose_name = 'Akun Permintaan Pembelian'
        verbose_name_plural = 'Akun Permintaan Pembelian'

    def status(self):
        ac = 0
        try:
            data = Detail_Purchase_Account.objects.filter(PO__id=self.id)
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
        b = Tr_Purchase_Pay.objects.filter(PO=instance)
        d = b.count()
    except:
        pass
    if d == 0 :
        Tr_Purchase_Pay.objects.create(PO=instance)

signals.post_save.connect(create_payment, sender=Payable_PO, weak=False, dispatch_uid='create_payment')

def create_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry, Tr_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.no_reg)
        n = a.count()
    except:
        pass
    if n == 0 :
        Tr_Journal_Entry.objects.create(Journal=instance.Journal, Journal_Period=instance.Period, Reference=instance.no_reg, Memo=instance.po_agreementx())
    else:
        Tr_Journal_Entry.objects.update(Journal=instance.Journal, Journal_Period=instance.Period, Reference=instance.no_reg, Memo=instance.po_agreementx())

signals.post_save.connect(create_Journal, sender=Payable_PO, weak=False, dispatch_uid='create_detail_Journal')

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
signals.post_delete.connect(delete_journal, sender=Payable_PO, weak=False, dispatch_uid='delete_Journal')
