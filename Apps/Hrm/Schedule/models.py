""" Develop By - Fery Febriyan Syah """


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from Apps.Hrm.Data_Personel_Management.models import Employee
from Apps.Hrm.Master_General.models import Department
from library.const.general import STATUS_PEGAWAI, SHIFT
from library.const.days import DAY_STATUS


class Header_Schedule (models.Model):
    date_now = models.DateField (verbose_name="Hari",)
    day_status = models.IntegerField (choices=DAY_STATUS, verbose_name="Status Hari",)
    employee_classification = models.IntegerField (choices=STATUS_PEGAWAI, verbose_name="Status Pegawai")
    Shift = models.IntegerField (choices=SHIFT, verbose_name="Shift Pegawai")
    lock = models.BooleanField (verbose_name="Kunci", 
                                help_text=')* Jangan Dicentang terlebih dahulu Sebelum Data Pegawai Di inputkan')
    
    class Meta:
        verbose_name = _('Penjadwalan Kerja')
        verbose_name_plural = _('Pendjawalan Kerja')
        ordering = ['id']
        
    
    def __unicode__(self):
        return '%s' % self.date_now


class Data_Schedule (models.Model):
    header = models.ForeignKey (Header_Schedule, verbose_name="Hari")
    employee = models.ForeignKey (Employee, verbose_name="Nama Pewagai")
    department = models.ForeignKey (Department, verbose_name="Departemen")
    
    class Meta:
        verbose_name = _('Data Pegawai')
        verbose_name_plural = _('Data Pegawai')
        ordering = ['id'] 
     
    def __unicode__(self):
        return '%s' % self.id
    
