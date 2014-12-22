"""Develop By - Achmad Afiffudin N"""

from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import signals, Max
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from datetime import datetime, timedelta
from Apps.Accounting.GeneralLedger.const import *
from decimal import *
from tinymce.models import HTMLField
from Apps.Accounting.AccountReceivable.const import *
from Apps.Asset.Master.models import *
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

class Ms_Account(MPTTModel):
    Account_Code = models.CharField(_('Kode Akun '), max_length=5, unique=True) 
    Account_Name = models.CharField(_('Nama Akun '), max_length=50)
    Account_Type = models.IntegerField(_('Tipe Akun '), choices=ACCOUNT_TYPE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name = 'children', verbose_name=_('Pilih Akar '),
    help_text='*) Pilih Akar Untuk Memetakan Akun berdasarkan Kode dan Tipe Akun')
    Status = models.BooleanField(_('Status'))
    order = models.IntegerField(_('Urutkan'))
    
    def __unicode__(self):
        return self.Account_Name

    class Meta:
        verbose_name = _('Master Akun')
        verbose_name_plural = _("Master Akun") 
        db_table = "FAGL | Master Akun"
    
    class MPTTMeta:
        order_insertion_by = ['order']

    def debit(self):
        total = 0
        try:         
            d = Detail_Journal_Entry.objects.filter(Account__id=self.id)
            for ds in d:
                total += ds.Debit
        except:
            pass
            
        return total
    debit.short_description = _('Debit')
    
    def credit(self):
        total = 0
        try: 
            d = Detail_Journal_Entry.objects.filter(Account__id=self.id)
            for ds in d:
                total += ds.Credit
        except:
            pass
            
        return total
    credit.short_description = _('Credit')
    
    def save(self, *args, **kwargs):
        super(Ms_Account, self).save(*args, **kwargs)
        Ms_Account.objects.rebuild()

"""
class Ms_Account(models.Model):
    Account_Code = models.CharField(_('Kode Akun'), max_length=5, unique=True) 
    Account_Name = models.CharField(_('Nama Akun'), max_length=50)
    Account_Type = models.IntegerField(_('Tipe Akun'), choices=ACCOUNT_TYPE)

    class Meta:
        verbose_name = _('Master Akun')
        verbose_name_plural = _('Master Akun')
        ordering = ['-id']

    def __unicode__(self):
        return '%(code)s - %(name)s' % {'code': self.Account_Code, 'name': self.Account_Name}

    def debit(self):
        total = 0
        try:         
            d = Detail_Journal_Entry.objects.filter(Account__id=self.id, Journal_Entry__Journal_Period__Fiscal_Year__Status=1)
            for ds in d:
                total += ds.Debit
        except:
            pass
            
        return total
    debit.short_description = _('Debit')
    
    def credit(self):
        total = 0
        try: 
            d = Detail_Journal_Entry.objects.filter(Account__id=self.id, Journal_Entry__Journal_Period__Fiscal_Year__Status=1)
            for ds in d:
                total += ds.Credit
        except:
            pass
            
        return total
    credit.short_description = _('Credit')

    def balance(self):
        total = 0
        try: 
            total = self.debit() - self.credit()
        except:
            pass
            
        return total
    balance.short_description = _('Balance')
        
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        models.Model.save(self, force_insert, force_update, using, update_fields)
"""    
class Ms_Fiscal_Years(models.Model):
    Code = models.CharField(_('Kode Fiskal'), max_length=25,unique=True) 
    Fiscal_Year = models.CharField(_('Nama Fiskal'), max_length=25) 
    Start_Fiscal = models.DateField(_('Mulai Tahun Fiskal'))
    End_Fiscal = models.DateField(_('Akhir Tahun Fiskal'))
    Status = models.IntegerField(_('Status'), choices=YEAR_STATUS, default=1)

    class Meta:
        verbose_name = _('Master Tahun Fiskal')
        verbose_name_plural = _('Master Tahun Fiskal')
        ordering = ['-Code']
        db_table = "FAGL | Master Fiskal"

    def __unicode__(self):
        return '%s' % self.Fiscal_Year

    def status(self):
        today = datetime.now().date()
        if today >= self.Start_Fiscal and today <= self.End_Fiscal:
            st=1
        else: st=2
        return st
        
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        today = datetime.now().date()
        if today >= self.Start_Fiscal and today <= self.End_Fiscal:
            self.Status=1
        else: self.Status=2
        models.Model.save(self, force_insert, force_update, using, update_fields)

class Ms_Period(models.Model):
    Code = models.CharField(verbose_name=_('Kode Periode'), max_length=25, unique=True)
    Period_Name = models.CharField(_('Nama Periode'), max_length=25)
    Fiscal_Year = models.ForeignKey(Ms_Fiscal_Years, verbose_name=_('Tahun Fiskal'))
    Start_Period = models.DateField(_('Mulai Periode'))
    End_Period = models.DateField(_('Akhir Periode'))
    Status = models.IntegerField(_('Status'), choices=PERIOD_STATUS, default=1)
    
    class Meta:
        verbose_name = _('Master Periode')
        verbose_name_plural = _('Master Periode')
        ordering = ['-id']
        db_table = "FAGL | Master Periode"

    def __unicode__(self):
        return '%s' % self.Period_Name
    
    def status(self):
        today = datetime.now().date()
        if today >= self.Start_Period and today <= self.End_Period:
            st=1
        else: st=2
        return st
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        today = datetime.now().date()
        if today >= self.Start_Period and today <= self.End_Period:
            self.Status=1        
        else: self.Status=2
        models.Model.save(self, force_insert, force_update, using, update_fields)

class Ms_Journal(models.Model):
    Code = models.CharField(_('Kode Jurnal'), max_length=25, unique=True)
    Journal_Name = models.CharField(_('Nama Jurnal'), max_length=25)
    Type = models.IntegerField(_('Tipe Jurnal'), choices=JOURNAL_TYPE)

    class Meta:
        verbose_name = _('Master Jurnal')
        verbose_name_plural = _('Master Jurnal')
        ordering = ['-id']
        db_table = "FAGL | Master Jurnal"

    def __unicode__(self):
        return self.Journal_Name

#penyusutan asset
class depresiation_record(models.Model):
    no_reg = models.CharField(verbose_name='No ', max_length=30, null=True, blank=True,
    help_text='*) Kosongkan form untuk mendapat Nomor otomatis')
    ref_asset = models.ForeignKey(Ms_asset, verbose_name=('Referen Asset '))
    dep_no = models.IntegerField(verbose_name=('Penyusuta ke '), blank=True, null=True)
    dep_value = models.DecimalField(verbose_name=('Nilai Penyusutan'), max_digits=20, decimal_places=2, blank=True, null=True)
    journal = models.ForeignKey(Ms_Journal, verbose_name=('Jurnal '), editable=False)
    period = models.ForeignKey(Ms_Period, verbose_name=('Periode '), editable=False)
	
    class Meta:
		verbose_name_plural="Penyusutan Aset"
		verbose_name="Penyusutan Aset"
		db_table = "FAGL | Penyusutan Aset"
	
    def __unicode__(self):
	    return '%s' % self.no_reg
        
    def no_rek(self):
        return '%(reg)s/0%(ke)s' % {'reg': self.ref_asset.no_reg, 'ke': self.dep_no}

    def periode(self):
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
            c = self.period
        return c
    
    def jurnal(self):
        a = Ms_Journal.objects.get(Type=6)
        return a

    def memo(self):
        return 'Dari Item %(reg)s, Penyusustan ke %(ke)s' % {'ke': self.dep_no,'reg': self.ref_asset.no_reg}
        
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.no_reg = self.no_rek()
        if self.no_reg == '':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_rek()
        self.journal = self.jurnal()
        self.period = self.periode()
        models.Model.save(self, force_insert, force_update, using, update_fields)

def create_journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.no_reg)
        n = a.count()
    except:
        pass
    if n == 0:
        Tr_Journal_Entry.objects.create(Journal=instance.journal, Journal_Period=instance.period, Reference=instance.no_reg, Memo=instance.memo())

signals.post_save.connect(create_journal, sender=depresiation_record, weak=False, dispatch_uid='create_Journal')

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    Detail_Journal_Entry.objects.filter(Reference=instance.Depreciation_Id).delete()
    Tr_Journal_Entry.objects.filter(Reference=instance.no_reg).delete()
signals.post_delete.connect(delete_journal, sender=depresiation_record, weak=False, dispatch_uid='delete_Journal')

class Detail_Depreciation_Account(models.Model):
    Depreciation = models.ForeignKey(depresiation_record, verbose_name=_('Penyusutan '))
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun '), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Akun Penyusutan')
        verbose_name_plural = _('Akun Penyusutan')
        ordering = ['-id']
        db_table = "FAGL | Akun Penyusutan Aset"

    def __unicode__(self):
        return '%s' % self.Depreciation

def create_detail_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry

    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Depreciation.no_reg)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Depreciation.no_reg, Account=instance.Account, Journal_Entry=j,  Debit=instance.Depreciation.dep_value, Credit=0)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Depreciation.no_reg, Account=instance.Account, Debit=instance.Depreciation.dep_value, Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Depreciation.no_reg)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Depreciation.no_reg, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Depreciation.dep_value)
            else:
                 Detail_Journal_Entry.objects.create(Reference=instance.Depreciation.no_reg, Account=instance.Account, Debit=0, Credit=instance.Depreciation.dep_value)
signals.post_save.connect(create_detail_Journal, sender=Detail_Depreciation_Account, weak=False, dispatch_uid='create_detail_Journal')

# Jurnal Penyesuaian
class Tr_Adjustment_Journal(models.Model):
    Adjustment_Journal_Id = models.CharField(verbose_name=_('No Jurnal Penyesuaian'), max_length=30, null=True, blank=True,
    help_text='*) Kosongkan form untuk mendapat Nomor otomatis')
    Date = models.DateField(_('Tanggal'), default=datetime.now())
    Journal = models.ForeignKey(Ms_Journal, verbose_name=_('Nama Jurnal'))
    Period = models.ForeignKey(Ms_Period, verbose_name=_('Periode '), editable=False)
    Memo = models.TextField(verbose_name=_('Catatan '), null=True, blank=True, max_length=50)
    Adjustment_Value = models.DecimalField(_('Nilai Penyesuaian'), max_digits=19, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('Jurnal Penyesuaian')
        verbose_name_plural = _('Jurnal Penyesuaian')
        ordering = ['-id']
        db_table = "FAGL | Jurnal Penyesuaian"

    def __unicode__(self):
        return self.Adjustment_Journal_Id
    
    def incstring(self):
        try:
            data = Tr_Adjustment_Journal.objects.all().order_by('Date')
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.Adjustment_Journal_Id).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring
	
    def inclen(self):
        leng = len(self.incstring())
        return leng
    
    def journal_id(self):
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
        return '%(prefix)s/%(year)s/%(month)s/%(unik)s' % {'prefix': 'PENY', 'year': intyear, 'month': strnow, 'unik': number}

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
        if self.Adjustment_Journal_Id == '':
            self.Adjustment_Journal_Id = self.journal_id()
        else: self.Adjustment_Journal_Id = self.Adjustment_Journal_Id
        self.Period = self.period()
        models.Model.save(self, force_insert, force_update, using, update_fields)

def create_journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    n=0
    try:
        a = Tr_Journal_Entry.objects.filter(Reference=instance.Adjustment_Journal_Id)
        n = a.count()
    except:
        pass
    if n == 0 :
        Tr_Journal_Entry.objects.create(Journal=instance.Journal, Journal_Period=instance.Period, Reference=instance.Adjustment_Journal_Id, Memo=instance.Memo)
    else:
        for d in a:
            d.Memo = instance.Memo
            d.save()
signals.post_save.connect(create_journal, sender=Tr_Adjustment_Journal, weak=False, dispatch_uid='create_Journal')

def delete_journal(sender,instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry, Detail_Journal_Entry
    Detail_Journal_Entry.objects.filter(Reference=instance.Adjustment_Journal_Id).delete()
    Tr_Journal_Entry.objects.filter(Reference=instance.Adjustment_Journal_Id).delete()
signals.post_delete.connect(delete_journal, sender=Tr_Adjustment_Journal, weak=False, dispatch_uid='delete_Journal')

#Akun Jurnal Penyesuaian
class Detail_Adjustment_Journal_Account(models.Model):
    Adjustment = models.ForeignKey(Tr_Adjustment_Journal, verbose_name=_('Jurnal Penyesuaian '))
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun '))
    Type = models.IntegerField(_('Tipe Akun '), choices=ACCOUNT_VALUE)

    class Meta:
        verbose_name = _('Akun Penyesuaian')
        verbose_name_plural = _('Akun Penyesuaian')
        ordering = ['-id']
        db_table = "FAGL | Akun Jurnal Akun Penyesuaian"

    def __unicode__(self):
        return '%s' % self.Adjustment

def create_detail_Journal(sender, created, instance, **kwargs):
    from Apps.Accounting.GeneralLedger.models import Detail_Journal_Entry
    from Apps.Accounting.GeneralLedger.models import Tr_Journal_Entry
    if created:
        if instance.Type == 1:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Adjustment.Adjustment_Journal_Id)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Adjustment.Adjustment_Journal_Id, Account=instance.Account, Journal_Entry=j,  Debit=instance.Adjustment.Adjustment_Value, Credit=0)
            else:
                Detail_Journal_Entry.objects.create(Reference=instance.Adjustment.Adjustment_Journal_Id, Account=instance.Account, Debit=instance.Adjustment.Adjustment_Value, Credit=0)
        else:
            b=0
            try:
                je = Tr_Journal_Entry.objects.filter(Reference=instance.Adjustment.Adjustment_Journal_Id)
                b = je.count()
            except:
                pass
            if b == 1:
                for j in je: Detail_Journal_Entry.objects.create(Reference=instance.Adjustment.Adjustment_Journal_Id, Account=instance.Account, Journal_Entry=j, Debit=0, Credit=instance.Adjustment.Adjustment_Value)
            else:
                 Detail_Journal_Entry.objects.create(Reference=instance.Adjustment.Adjustment_Journal_Id, Account=instance.Account, Debit=0, Credit=instance.Adjustment.Adjustment_Value)
signals.post_save.connect(create_detail_Journal, sender=Detail_Adjustment_Journal_Account, weak=False, dispatch_uid='create_detail_Journal')

#Jurnal Entry    
class Tr_Journal_Entry(models.Model):
    Journal_Entry_No = models.CharField(_('Nomor Jurnal Entry'), blank=True, null=True, max_length=25, unique=False, default='')
    Reference = models.CharField(_('Referensi'), max_length=25, blank=True, null=True)
    Date = models.DateField(_('Tanggal'),default=datetime.now())
    Journal = models.ForeignKey(Ms_Journal, verbose_name=_('Nama Jurnal'))
    Journal_Period = models.ForeignKey(Ms_Period, verbose_name=_('Periode Jurnal'))
    Debit = models.DecimalField(_('Total Debit'), max_digits=19, decimal_places=2, blank=True, null=True, default=0)
    Credit = models.DecimalField(_('Total Kredit'), max_digits=19, decimal_places=2, blank=True, null=True, default=0)
    Memo = HTMLField(verbose_name='Catatan ', blank=True)
    Status = models.IntegerField(_('Status'), choices=JOURNAL_STATUS, default=1)

    class Meta:
        verbose_name = _('Entri Jurnal')
        verbose_name_plural = _('Entri Jurnal')
        ordering = ['-Date']
        db_table = "FAGL | Jurnal Entri"

    def __unicode__(self):
        return self.Journal_Entry_No

    def memo(self):
        return u'%s' % self.Memo
    memo.allow_tags = True
    memo.short_description = _('Catatan ')

    def incstring(self):
        try:
            data = Tr_Journal_Entry.objects.all().order_by('Date')
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.Journal_Entry_No).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring
	
    def inclen(self):
        leng = len(self.incstring())
        return leng
    
    def journal_id(self):
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
        return '%(year)s/%(month)s/%(prefix)s/%(unik)s' % {'prefix': self.Journal.Code, 'year': intyear, 'month': strnow, 'unik': number}

    def debit(self):
        total = 0
        try:
            d = Detail_Journal_Entry.objects.filter(Journal_Entry__id=self.id)
            for ds in d:
                total += ds.Debit
        except:
            pass
            
        return total
    debit.short_description = _('Total Debit')
    
    def credit(self):
        total = 0
        try: 
            d = Detail_Journal_Entry.objects.filter(Journal_Entry__id=self.id)
            for ds in d:
                total += ds.Credit
        except:
            pass
            
        return total
    credit.short_description = _('Total Credit')
        
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.Debit = self.debit()
        self.Credit = self.credit()
        if self.Journal_Entry_No == '':
            self.Journal_Entry_No = self.journal_id()
        else: self.Journal_Entry_No = self.Journal_Entry_No
        models.Model.save(self, force_insert, force_update, using, update_fields)

#Detail Jurnal Entry
class Detail_Journal_Entry(models.Model):
    Date = models.DateField(_('Tanggal'),default=datetime.now())
    Reference = models.CharField(_('Referensi'), max_length=25, blank=True, null=True)    
    Account = models.ForeignKey(Ms_Account, verbose_name=_('Akun'))
    Journal_Entry = models.ForeignKey(Tr_Journal_Entry, verbose_name=_('Jurnal Entri'))
    Debit = models.DecimalField(_('Debit'), max_digits=19, decimal_places=2, blank=True, null=True, default=0)
    Credit = models.DecimalField(_('Kredit'), max_digits=19, decimal_places=2, blank=True, null=True, default=0)

    class Meta:
        verbose_name = _('Jurnal Item')
        verbose_name_plural = _('Jurnal Item')
        ordering = ['-id']
        db_table = "FAGL | Detail Jurnal Entri"

    def __unicode__(self):
        return '%(ref)s | %(ak)s' % {'ref': self.Reference, 'ak': self.Account}
