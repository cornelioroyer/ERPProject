__author__ = 'FARID ILHAM Al-Q'

from django.contrib.auth.models import User
from library.const.customer import *
from library.const.country import *
from django.utils.translation import ugettext_lazy as _
from django.db import models
from PIL import Image
from django.conf import settings

class UserCompany(User):
    class Meta:
        proxy = True
        verbose_name = _("Akun Perusahaan")
        verbose_name_plural = _("Akun Perusahaan")


class Company(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=_('Username '), limit_choices_to={'is_staff': False})
    name = models.CharField(verbose_name=_('Nama '), max_length=100,
                            help_text=_('*) Isi dengan nama pegawai yang bersangkutan.'))
    email = models.EmailField(verbose_name=_('Email '), max_length=100,
                              help_text=_('*) Isi dengan Email aktif perusahaan.'))
    position = models.CharField(verbose_name=_('Jabatan '), max_length=100, blank=True,
                                help_text=_('*) Jabatan pegawai yang bersangkutan.'))
    corporate = models.CharField(verbose_name=_('Perusahaan '), max_length=254,
                                 help_text=_('*) Nama perusahaan lengkap. Tanpa bentuk usaha.'))
    business = models.CharField(verbose_name=_('Kegiatan Bisnis '), max_length=100, choices=BISNIS)
    industry = models.CharField(verbose_name=_('Bidang Industri '), max_length=100, choices=INDUSTRI)
    type = models.CharField(verbose_name=_('Jenis Perusahaan '), max_length=100, choices=TYPE_BISNIS)
    address = models.TextField(verbose_name=_('Alamat '), help_text=_('*) Alamat lengkap perusahaan.'))
    zip_code = models.IntegerField(verbose_name=_('Kode Pos '), max_length=10)
    region = models.CharField(verbose_name=_('Regional'), max_length=100, choices=REGION, blank=True, null=True)
    country = models.CharField(verbose_name=_('Negara '), max_length=100, choices=[(x[0], x[3]) for x in COUNTRIES])
    city = models.CharField(verbose_name=_('Kota '), max_length=100, blank=True)
    province = models.CharField(verbose_name=_('Provinsi '), max_length=100, blank=True)
    npwp = models.CharField(verbose_name=_('N.P.W.P '), max_length=100, blank=True,
                            help_text=_('*) Isi dengan N.P.W.P perusahaan yang sesuai.'))
    phone = models.CharField(verbose_name=_('Telepon '), max_length=20,
                             help_text=_('*) Nomer telepon valid yang bisa dihubungi. ex: 087750000149'))
    fax = models.CharField(verbose_name=_('Fax '), max_length=20, blank=True)
    website = models.URLField(verbose_name=_('Website '), blank=True, help_text=_('*) Website perusahaan (jika ada). '
                                                                                  'Ex: http://www.example.com'))
    logo = models.ImageField(verbose_name=_('Logo Perusahaan '), upload_to='uploads/logo/company', blank=True,
                             default='uploads/default.jpg')
    currency = models.ForeignKey("CashBank.Ms_Currency", verbose_name=_('Mata Uang '), blank=True, null=True,
                                 help_text="*) Mata uang yang digunakan.")
    bank_name = models.ForeignKey("CashBank.Ms_Bank", verbose_name=_('Nama Bank '), blank=True, null=True)
    bank_branch = models.CharField(verbose_name=_('Cabang '), max_length=250, blank=True,
                                   help_text=_('*) ex: Jakarta, Surabaya, others.'))
    bank_account_name = models.CharField(verbose_name=_('Atas Nama '), max_length=250, blank=True,
                                         help_text=_('*) Nama lengkap dalam rekening.'))
    rek = models.CharField(verbose_name=_('No. Rekening '), max_length=250, blank=True,
                           help_text=_('*) Masukkan nomer rekening, ex: 1234567890.'))

    class Meta:
        verbose_name = _('Data Perusahaan')
        verbose_name_plural = _('Data Perusahaan')
        ordering = ["-user__date_joined"]

    def type_com(self):
        if self.type == "1":
            a = "PT."
        elif self.type == "2":
            a = "CV."
        elif self.type == "3":
            a = "Fa."
        elif self.type == "4":
            a = "(None)"
        return a

    def __unicode__(self):
        return "%(type)s %(na)s" % {"type": self.type_com(), "na": self.corporate}

    def display_image(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="75"/>' % (settings.MEDIA_URL, self.logo)

    display_image.short_description = 'Foto'
    display_image.allow_tags = True

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):

        if not self.logo:
            return

        super(Company, self).save()
        logo = Image.open(self.logo)
        (width, height) = logo.size
        size = (110, 110)
        logo = logo.resize(size, Image.ANTIALIAS)
        logo.save(self.logo.path)
        data = User.objects.filter(username=self.user).update(email=self.email)
        return data

from django.db.models.signals import post_delete

def delete_related_user(sender, **kwargs):
    deleted_profile = kwargs['instance']
    deleted_profile.user.delete()

post_delete.connect(delete_related_user, sender=Company)
