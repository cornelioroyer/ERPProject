"""Develop By - Fery Febriyan Syah"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import intcomma
from Apps.Hrm.Master_General.models import Master_Position, Bank
from Apps.Distribution.master_sales.models import Currency
from Apps.Hrm.Data_Personel_Management.models import Employee
from datetime import datetime
from library.const.group import GROUP


class Operational_Support (models.Model):
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    currency = models.ForeignKey (Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    total_operasional_support = models.FloatField (max_length=20, verbose_name="Jumlah Tunjangan",)
    
    class Meta:
        verbose_name = _('Tunjangan Operasional')
        verbose_name_plural = _('Tunjangan Operasional')
        ordering = ['id']
       
    def get_total_price(self):
        return intcomma(self.total_operasional_support)
    
    def display_price(self):
        st = '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': self.get_total_price(), 'back': self.currency.post_symbol}
        return st 
    
    def __unicode__(self):
        return '%s' % intcomma(self.total_operasional_support)
    
    display_price.short_description = _('Jumlah Tunjangan')
    
    
class Shift_Operational_Support (models.Model):
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    currency = models.ForeignKey (Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    total_shift_operasional_support = models.FloatField (max_length=20, verbose_name="Jumlah Tunjangan", )
    
    class Meta:
        verbose_name = _('Tunjangan Operasional Shift')
        verbose_name_plural = _('Tunjangan Operasional Shift')
        ordering = ['id']
 
    def get_total_price(self):
        return intcomma(self.total_shift_operasional_support)
       
    def display_price(self):
        st = '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': self.get_total_price(), 'back': self.currency.post_symbol}
        return st 
    
    def __unicode__(self):
        return '%s' % intcomma(self.total_shift_operasional_support)
    
    display_price.short_description = _('Jumlah Tunjangan')
    
    
class Shift_Operational_Supporting (models.Model):
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    currency = models.ForeignKey (Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    total_shift_operasional_supporting = models.FloatField (max_length=20, verbose_name="Jumlah Tunjangan")
    
    class Meta:
        verbose_name = _('Tunjangan Penunjang Operasional Shift')
        verbose_name_plural = _('Tunjangan Penunjang Operasional Shift')
        ordering = ['id']
    
    def get_total_price(self):
        return intcomma(self.total_shift_operasional_supporting)
       
    def display_price(self):
        st = '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': self.get_total_price(), 'back': self.currency.post_symbol}
        return st 
       
    def __unicode__(self):
        return '%s' % intcomma(self.total_shift_operasional_supporting)
    
    display_price.short_description = _('Jumlah Tunjangan')
    
class Position_Support (models.Model):
    master_position = models.ForeignKey (Master_Position, verbose_name="Jabatan")
    currency = models.ForeignKey (Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    total_position_support = models.FloatField (max_length=20, verbose_name="Jumlah Tunjangan")
    
    class Meta:
        verbose_name = _('Tunjangan Jabatan')
        verbose_name_plural = _('Tunjangan Jabatan')
        ordering = ['id']
    
    def get_total_price(self):
        return intcomma(self.total_position_support)
    
    def display_price(self):
        st = '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': self.get_total_price(), 'back': self.currency.post_symbol}
        return st 
  
    def __unicode__(self):
        return '%s' % intcomma(self.total_position_support)
    
    display_price.short_description = _('Jumlah Tunjangan')
    
    
class Life_Cost_Support (models.Model):
    master_position = models.ForeignKey (Master_Position, verbose_name="Jabatan")
    currency = models.ForeignKey (Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    total_life_support = models.FloatField (max_length=20, verbose_name="Jumlah Tunjangan")
    
    class Meta:
        verbose_name = _('Tunjangan Biaya Hidup')
        verbose_name_plural = _('Tunjangan Biaya Hidup')
        ordering = ['id']
    
    def get_total_price(self):
        return intcomma(self.total_life_support)
    
    def display_price(self):
        st = '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': self.get_total_price(), 'back': self.currency.post_symbol}
        return st 
    
    def __unicode__(self):
        return '%s' % intcomma(self.total_life_support)
    
    display_price.short_description = _('Jumlah Tunjangan')
    
    
class Transport_Support (models.Model):
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    currency = models.ForeignKey (Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    total_transport_support = models.FloatField (max_length=20, verbose_name="Jumlah Tunjangan")
    
    class Meta:
        verbose_name = _('Tunjangan transport')
        verbose_name_plural = _('Tunjangan transport')
        ordering = ['id']
    
    def get_total_price(self):
        return intcomma(self.total_transport_support)
    
    def display_price(self):
        st = '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': self.get_total_price(), 'back': self.currency.post_symbol}
        return st 
    
    def __unicode__(self):
        return '%s' % intcomma(self.total_transport_support)

    display_price.short_description = _('Jumlah Tunjangan')


class Basic_Salary (models.Model):
    group = models.IntegerField (choices=GROUP, verbose_name="Golongan")
    currency = models.ForeignKey (Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    total_basic_salary = models.FloatField (max_length=20, verbose_name="Jumlah Gaji Pokok")
    
    class Meta:
        verbose_name = _('Gaji Pokok')
        verbose_name_plural = _('Gaji Pokok')
        ordering = ['id']
    
    def get_total_price(self):
        return intcomma(self.total_basic_salary)
    
    def display_price(self):
        st = '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': self.get_total_price(), 'back': self.currency.post_symbol}
        return st 
    
    def __unicode__(self):
        return '%s' % intcomma(self.total_basic_salary)
    
    display_price.short_description = _('Jumlah Tunjangan')
    
    
class Credit_Bank (models.Model):
    name = models.CharField (max_length=50, verbose_name="Nama Pinjaman")
    currency = models.ForeignKey (Currency, verbose_name=_('Mata Uang '), max_length=50, default=1)
    total_loan = models.FloatField (max_length=20, verbose_name="Jumlah Pinjaman")
    name_bank = models.ForeignKey (Bank, verbose_name="Nama Bank")
    
    class Meta:
        verbose_name = _('Pinjaman Bank')
        verbose_name_plural = _('Pinjaman Bank')
        ordering = ['id']
    
    def get_total_price(self):
        return intcomma(self.total_loan)
    
    def display_price(self):
        st = '%(logo)s %(price)s%(back)s' % {'logo': self.currency.pre_symbol, 'price': self.get_total_price(), 'back': self.currency.post_symbol}
        return st 
    
    def __unicode__(self):
        return '%s' % intcomma(self.total_loan)
    
    display_price.short_description = _('Jumlah Tunjangan')
    
"""    
class Overtime (models.Model):
    month = models.CharField (max_length=6, verbose_name="Bulan", editable=False)
    employee = models.ForeignKey (Employee, verbose_name="Nama Pegawai") 
    duration_overtime = models.IntegerField (verbose_name="Jumlah Lembur", help_text=_('*) Satuan Menit'))
      
    class Meta:
        verbose_name = _('Lembur')
        verbose_name_plural = _('Lembur')
        ordering = ['id']
    
    def bln (self):
        now = datetime.now()
        nowm = now.strftime("%m")
        nowy = now.strftime("%Y")
        strnow = '%(y)s%(m)s' % {'y':nowy,'m':nowm}
        return strnow
    
    def save (self, force_insert=False, force_update=False, using=None):
        if self.month == '':
            self.month = self.bln()
        else: self.month = self.month
        super (Overtime,self).save()
    
    def __unicode__(self):
        return '%s' % self.id
    
class Set_of_Overtime (models.Model):
    low = models.IntegerField (verbose_name="Rendah")
    high = models.IntegerField (verbose_name="Tinggi")
    precentage = models.DecimalField (max_digits=4, verbose_name="Persentase", decimal_places=3)
    
    class Meta:
        verbose_name = _('Persentase Lembur')
        verbose_name_plural = _('Persentase Lembur')
        ordering = ['id']
    
    def __unicode__(self):
        return '%s' % self.id
"""
    
    
    
