__author__ = 'FARID ILHAM Al-Q'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


class Tax(models.Model):
    name = models.CharField(_('Nama '), max_length=50)
    description = models.TextField(_('Deskripsi '), blank=True)
    percentage = models.DecimalField(_('Persentase '), max_digits=4, decimal_places=1, default=0,
                                     help_text=_('*) Persentase pajak dalam angka'))

    class Meta:
        verbose_name = _('Pajak')
        verbose_name_plural = _('Pajak')
        db_table = "Distribusi | Pajak"

    def __unicode__(self):
        return '%(nama)s %(persen)s %(per)s' % {'nama': self.name, 'persen': self.percentage, 'per': '%'}


class Currency(models.Model):
    name = models.CharField(verbose_name=_('Nama '), max_length=50)
    code = models.CharField(verbose_name=_('Kode '), unique=True, max_length=3)
    rate = models.DecimalField(verbose_name=_('Kurs '), max_digits=12, decimal_places=2, blank=True)
    pre_symbol = models.CharField(verbose_name=_('Pre-Simbol '), blank=True, max_length=3)
    post_symbol = models.CharField(verbose_name=_('Post-Simbol '), blank=True, max_length=3)

    class Meta:
        verbose_name = _('Mata Uang')
        verbose_name_plural = _('Mata Uang')
        db_table = "Distribusi | Mata Uang"

    def __unicode__(self):
        return self.name


class PaymentTerm(models.Model):
    name = models.CharField(verbose_name=_('Nama '), max_length=50)
    description = models.TextField(verbose_name=_('Deskripsi '), blank=True)
    period = models.IntegerField(verbose_name=_('Jangka Waktu '))

    class Meta:
        verbose_name = _('Waktu Pembayaran')
        verbose_name_plural = _('Waktu Pembayaran')
        ordering = ['id']
        db_table = "Distribusi | Waktu Pembayaran"

    def __unicode__(self):
        return '%s hari' % self.period


class Bank(models.Model):
    name = models.CharField(verbose_name=_('Nama'), max_length=50, blank=True)
    description = models.TextField(verbose_name=_('Deskripsi'))
    logo = models.ImageField(verbose_name=_('Logo'), upload_to='uploads/logo/bank', blank=True,
                             default='uploads/default.jpg')

    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Bank')
        db_table = "Distribusi | Bank"

    def display_image(self):
        return '<img src="/media/%s" WIDTH="75" HEIGHT="75"/>' % self.logo
    display_image.short_description = 'Logo'
    display_image.allow_tags = True

    def __unicode__(self):
        return self.name


class ShippingMethods(models.Model):
    name = models.CharField(verbose_name=_('Nama '), max_length=50)
    info = models.TextField(verbose_name=_('Keterangan '), blank=True)

    class Meta:
        verbose_name = _('Metode Pengiriman ')
        verbose_name_plural = _('Metode Pengiriman ')
        db_table = "Distribusi | Metode Pengiriman"

    def __unicode__(self):
        return self.name


categoryCall = {('1', 'Panggilan Masuk'),('2', 'Panggilan Keluar')}
priorityCall = {('1', 'Rendah'), ('2', 'Normal'), ('3', 'Tinggi')}
statusCall = {('1', 'Logged Call'), ('2', 'Scheduled'), ('3', 'Not Held')}

from Apps.Distribution.customer.models import Company


class LogCall(models.Model):
    customer = models.ForeignKey(Company, verbose_name=_('Nama Perusahaan '))
    date = models.DateTimeField(verbose_name=_('Tanggal Panggilan '), default=datetime.now())
    duration = models.CharField(verbose_name=_('Durasi '), max_length=50, default='00:00', help_text=_('*) format durasi (HH:MM:SS) ex: 01:30 atau 1 menit 30 detik'))
    category = models.CharField(verbose_name=_('Kategori '), max_length=50, choices=categoryCall)
    priority = models.CharField(verbose_name=_('Prioritas '), max_length=50, choices=priorityCall)
    summary = models.CharField(verbose_name=_('Ringkasan Panggilan '), max_length=50, help_text=_('*) Ringkasan dari hasil panggilan'))
    status = models.CharField(verbose_name=_('Status '), max_length=50, choices=statusCall)

    class Meta:
        verbose_name_plural = _('Daftar Panggilan')
        verbose_name = _('Panggilan')
        db_table = "Distribusi | Logged Call"

    def __unicode__(self):
        return self.customer.corporate

    def cust_name(self):
        return self.customer.name
    cust_name.short_description = _('Nama')

    def no_phone(self):
        return self.customer.phone
    no_phone.short_description = _('No. Telepon')


class ScheduledCall(LogCall):

    class Meta:
        proxy = True
        verbose_name_plural = _('Panggilan Terjadwal')
        verbose_name = _('Panggilan ')
        db_table = "Distribusi | Scheduled Call"


from django.contrib.auth.models import User
from Apps.Hrm.Data_Personel_Management.models import Employee


class StaffPerson(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Username"), unique=True, limit_choices_to={'is_staff': True, 'is_superuser': False},)
    employee = models.ForeignKey(Employee, verbose_name=_('Nama Pegawai'))
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"
        ordering = ["id"]
        db_table = "Distribusi | Manage Staff"

    def department(self):
        return self.employee.department
    department.short_description = 'Departemen'

    def section(self):
        return self.employee.section
    section.short_description = 'Jabatan'

    def __unicode__(self):
        return "%(name)s (%(id)s)" % {'id': self.user, 'name':self.employee.employee}
