from django.db import models
from django.contrib.auth.models import User
from library.const.Gudang import LEVEL_AKSES
from django.db.models.signals import post_save
from django.db.models import signals
from django.utils.translation import ugettext as _


class Jenis_satuan (models.Model):
    type_satuan = models.CharField (max_length=50, verbose_name="Jenis Satuan")
    
    class Meta:
        verbose_name_plural= _('Jenis Satuan')
        verbose_name= _('Jenis Satuan')
    
    def __unicode__(self):
            return u'%s' % self.type_satuan
       
class type_commodity (models.Model):
    type_commodity = models.CharField (max_length=50, verbose_name="Jenis Barang")
    
    class Meta:
        verbose_name_plural= _('Jenis Barang')
        verbose_name= _('Jenis Barang')
        
    def __unicode__(self):
        return u'%s' % self.type_commodity
                
class quantity_commodity (models.Model):
    quantity_commodity = models.CharField (max_length=50, verbose_name="Kualitas Barang")
    
    class Meta:
        verbose_name_plural= _('Kualitas Barang')
        verbose_name= _('Kualitas Barang')
        
    def __unicode__(self):
        return u'%s' % self.quantity_commodity
        

class Department (models.Model):
    department = models.CharField (max_length=50, verbose_name="Departemen")
    
    class Meta:
        verbose_name = _('Departemen')
        verbose_name_plural = _('Departemen')
        ordering = ['id']
        
    def __unicode__(self):
        return u'%s' % self.department

    
class Role_user(models.Model):
    user = models.OneToOneField(User, related_name='user akses')
    access_level = models.CharField(max_length=30, choices=LEVEL_AKSES, verbose_name='Level Akses')
    position = models.CharField(max_length=30, blank=True, null=True, verbose_name='Jabatan')
    intern_date_register = models.DateField(auto_now_add=True, verbose_name='Tanggal Daftar')
#    department = models.ForeignKey(Department, blank=True, null=True, verbose_name='Departemen')
    
    class Meta:
        verbose_name = _('Hak Akses')
        verbose_name_plural = _('Hak Akses')
        ordering = ['id']
    
    def __unicode__(self):
        return u"%s" % self.user

def create_user_profile(sender, instance, created, **kwargs):  
    if created == True:  
        profile, created = Role_user.objects.get_or_create(user=instance)
        
post_save.connect(create_user_profile, sender=User)
