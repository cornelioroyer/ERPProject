from django.db import models
#from Apps.Procurement.vendor.const.const import *
from django.contrib.auth.models import User
from datetime import datetime
#from Apps.Procurement.internal.models import *

class Classification(models.Model):
    classification_detail = models.CharField(verbose_name='Klasifikasi', max_length=50)

    class Meta:
        verbose_name = 'Klasifikasi'
        verbose_name_plural = 'Klasifikasi'

    def __unicode__(self):
        return '%s' % self.classification_detail

class Fields(models.Model):
    fields_detail = models.CharField(verbose_name='Bidang', max_length=50)

    class Meta:
        verbose_name = 'Bidang'
        verbose_name_plural = 'Bidang'

    def __unicode__(self):
        return '%s' % self.fields_detail

class Sub_Fields(models.Model):
    sub_fields_detail = models.CharField(verbose_name='Sub Bidang', max_length=50)
    class Meta:
        verbose_name = 'Sub Bidang'
        verbose_name_plural = 'Sub Bidang'

    def __unicode__(self):
        return '%s' % self.sub_fields_detail

class Goods_Type(models.Model):
    goods_type_detail = models.CharField(verbose_name='Keterangan', max_length=20)

    class Meta:
        verbose_name = 'Jenis Barang'
        verbose_name_plural = 'Jenis Barang'
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.goods_type_detail

class Unit_Of_Measure(models.Model):
    unit_of_measure_detail = models.CharField(verbose_name='Nama Satuan', max_length=20)

    class Meta:
        verbose_name = 'Satuan Barang'
        verbose_name_plural = 'Satuan Barang'
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.unit_of_measure_detail

class Set_Of_Delay(models.Model):
    value = models.CharField(verbose_name='Nilai Hari', max_length=30)
    set_of_delay_detail = models.CharField(verbose_name='Label', max_length=30)

    class Meta:
        verbose_name = 'Satuan Keterlambatan'
        verbose_name_plural = 'Satuan Keterlambatan'
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.set_of_delay_detail

class Currency(models.Model):
    currency_symbol = models.CharField(verbose_name='Simbol', max_length=5)
    currency_name = models.CharField(verbose_name='Mata Uang', max_length=20)
    currency_rate = models.DecimalField(verbose_name='Nilai Tukar', decimal_places=2, max_digits=10, default=1)

    class Meta:
        verbose_name = 'Mata Uang'
        verbose_name_plural = 'Mata Uang'
        ordering = ['id']

    def __unicode__(self):
        return '%s' % self.currency_symbol