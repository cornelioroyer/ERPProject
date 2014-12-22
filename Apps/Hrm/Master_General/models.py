""" Develop By - Fery Febriyan Syah """


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from library.const.general import LEVEL_AKSES
from django.db.models.signals import post_save
from django.db.models import signals



class Department (models.Model):
    department = models.CharField (max_length=50, verbose_name="Departemen")
    
    class Meta:
        verbose_name = _('Departemen')
        verbose_name_plural = _('Departemen')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.department


class Level_Position (models.Model):
    level_position = models.CharField (max_length=50, verbose_name="Tingkat Jabatan")
    
    class Meta:
        verbose_name = _('Tingkat Jabatan')
        verbose_name_plural = _('Tingkat Jabatan')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.level_position
    
    
class Section (models.Model):
    section = models.CharField (max_length=50, verbose_name="Seksi")
    
    class Meta:
        verbose_name = _('Seksi')
        verbose_name_plural = _('Seksi')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.section
    

class Master_Position (models.Model):
    master_position = models.CharField (max_length=50, verbose_name="Jabatan")
    
    class Meta:
        verbose_name = _('Jabatan')
        verbose_name_plural = _('Jabatan')
        ordering = ['id']
        
    def __unicode__(self):
        return '%s' % self.master_position
    

class Bank (models.Model):
    name_bank = models.CharField (max_length=50, verbose_name="Nama bank")
    address = models.CharField (max_length=50, verbose_name="Alamat bank")
    
    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Bank')
        ordering = ['id']
    
    def __unicode__(self):
        return '%s' % self.name_bank
"""    
class Currency(models.Model):
    name = models.CharField(verbose_name=_('Nama '), max_length=50)
    code = models.CharField(verbose_name=_('Kode '), unique=True, max_length=3)
    rate = models.DecimalField(verbose_name=_('Kurs '), max_digits=12, decimal_places=2, blank=True)
    pre_symbol = models.CharField(verbose_name=_('Pre-Simbol '), blank=True, max_length=3)
    post_symbol = models.CharField(verbose_name=_('Post-Simbol '), blank=True, max_length=3)

    class Meta:
        verbose_name = _('Mata Uang')
        verbose_name_plural = _('Mata Uang')
        ordering = ['id']

    def __unicode__(self):
        return self.name
"""    

class Role_user(models.Model):
    user = models.OneToOneField(User, related_name=_("user"))
    access_level = models.CharField(max_length=30, choices=LEVEL_AKSES, verbose_name='Level Akses')
    position = models.CharField(max_length=30, blank=True, null=True, verbose_name='Jabatan')
    intern_date_register = models.DateField(auto_now_add=True, verbose_name='Tanggal Daftar')
    department = models.ForeignKey(Department, blank=True, null=True, verbose_name='Departemen')
    
    class Meta:
        verbose_name = 'Hak Akses'
        verbose_name_plural = 'Hak Akses'
        ordering = ['id']
    
    def __unicode__(self):
        return "%s" % self.user

def create_user_profile(sender, instance, created, **kwargs):  
    if created == True:  
        profile, created = Role_user.objects.get_or_create(user=instance)
        
post_save.connect(create_user_profile, sender=User)

