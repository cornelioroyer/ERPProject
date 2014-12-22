""" Develop By - Fery Febriyan Syah """

from django.db import models
from django.utils.translation import ugettext_lazy as _
from library.const.general import RELIGION, GENDER, NATIONAL, BLOOD, EDU_STATUS, STATUS
from library.const.province import PROVINCE
from tinymce.models import HTMLField


class Wife (models.Model):
    wife_name = models.CharField (max_length=20, verbose_name="Nama Istri")
    birthday = models.DateField (max_length=20, verbose_name="Tanggal Lahir")
    religion = models.IntegerField (choices=RELIGION, max_length=1, verbose_name="Agama")
    national = models.IntegerField(choices=NATIONAL, max_length=1, verbose_name="Kewarganegaraan")
    province = models.IntegerField (choices=PROVINCE, max_length=1, verbose_name="Provinsi")
    address = HTMLField (max_length=50, verbose_name="Alamat", help_text=(' *)Alamat Lengkap'))
    work = models.CharField (max_length=50, blank=True, verbose_name="Pekerjaan")
    blood_group = models.IntegerField (choices=BLOOD, max_length=1, verbose_name="Golongan Darah")
     
    class Meta:
        verbose_name = _('Data Istri')
        verbose_name_plural = _('Data Istri')
        ordering = ['id']
        
    def addressx(self):
        return '%s' % self.address
    addressx.allow_tags = True
    addressx.short_description = 'Alamat'
        
    def ___unicode__(self):
        return '%s' % self.wife_name


class Child1 (models.Model):
    child_name_1 = models.CharField (max_length=20, blank=False, verbose_name="Nama Anak Pertama")
    birthday = models.DateField (max_length=20, blank=True, verbose_name="Tanggal Lahir")
    religion = models.IntegerField (choices=RELIGION, max_length=1, verbose_name="Agama")
    gender = models.IntegerField (choices=GENDER, max_length=1, blank=True, verbose_name="Jenis Kelamin")
    work = models.CharField (max_length=50, verbose_name="Pekerjaan")
    education_status = models.CharField (choices=EDU_STATUS, max_length=1, verbose_name="status Pendidikan")
    status = models.IntegerField (choices=STATUS, max_length=1, help_text=(' *)Status Perkawinan'))
    blood_group = models.IntegerField (choices=BLOOD, max_length=1, verbose_name="Golongan Darah")
    
    class Meta:
        verbose_name = _('Data Anak Pertama')
        verbose_name_plural = _('Data Anak Pertama')
        ordering = ['id']
        
        
    def __unicode__(self):
        return '%s' % self.child_name_1

class Child2 (models.Model):
    child_name_2 = models.CharField (max_length=20, blank=False, verbose_name="Nama Anak Kedua")
    birthday = models.DateField (max_length=20, blank=True, verbose_name="Tanggal Lahir")
    religion = models.IntegerField (choices=RELIGION, max_length=1, verbose_name="Agama")
    gender = models.IntegerField (choices=GENDER, max_length=1, blank=True, verbose_name="Jenis Kelamin")
    work = models.CharField (max_length=50, verbose_name="Pekerjaan")
    education_status = models.IntegerField (choices=EDU_STATUS, max_length=1, verbose_name="status Pendidikan")
    status = models.IntegerField (choices=STATUS, max_length=1, help_text=(' *)Status Perkawinan'))
    blood_group = models.IntegerField (choices=BLOOD, max_length=1, verbose_name="Golongan Darah")

    class Meta:
        verbose_name = _('Data Anak Kedua')
        verbose_name_plural = _('Data Anak Kedua')
        ordering = ['id']
        
        
    def __unicode__(self):
        return '%s' % self.child_name_2
    
class Parent1 (models.Model):
    father_name = models.CharField (max_length=50, blank=False, verbose_name="Nama Ayah")
    birthday = models.DateField (max_length=20, blank=True, verbose_name="Tanggal Lahir")
    religion = models.IntegerField (choices=RELIGION, max_length=1, verbose_name="Agama")
    national = models.IntegerField(choices=NATIONAL, max_length=1, verbose_name="Kewarganegaraan")
    province = models.IntegerField (choices=PROVINCE, max_length=1, verbose_name="Provinsi")
    address = HTMLField (max_length=50, verbose_name="Alamat", help_text=(' *)Alamat Lengkap'))
    
    
    class Meta:
        verbose_name = _('Data Ayah')
        verbose_name_plural = _('Data Ayah')
        ordering = ['id']
    
    def addressx(self):
        return '%s' % self.address
    addressx.allow_tags = True
    addressx.short_description = 'Alamat'    
        
    def __unicode__(self):
        return '%s' % self.father_name

class Parent2 (models.Model):
    mather_name = models.CharField (max_length=50, blank=False, verbose_name="Nama Ibu")
    birthday = models.DateField (max_length=20, blank=True, verbose_name="Tanggal Lahir")
    national = models.IntegerField(choices=NATIONAL, max_length=1, verbose_name="Kewarganegaraan")
    province = models.IntegerField (choices=PROVINCE, max_length=1, verbose_name="Provinsi")
    address = HTMLField (max_length=50, verbose_name="Alamat", help_text=(' *)Alamat Lengkap'))
    
    
    class Meta:
        verbose_name = _('Data Ibu')
        verbose_name_plural = _('Data Ibu')
        ordering = ['id']
        
    def addressx(self):
        return '%s' % self.address
    addressx.allow_tags = True
    addressx.short_description = 'Alamat'
        
    def ___unicode__(self):
        return '%s' % self.mather_name
