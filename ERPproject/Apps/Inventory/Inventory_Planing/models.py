from django.db import models
from django.utils.translation import ugettext as _
from Apps.Inventory.Inventory_Planing import *
from library.const.Gudang import GROUP
from tinymce.models import HTMLField
from Apps.Inventory.Property_Inv.models import *


class Warehouse(models.Model):
    code_warehouse = models.CharField (max_length=50, verbose_name="Kode Gudang")
    warehouse_name = models.CharField (max_length=50, verbose_name="Nama Gudang")
    type_warehouse = models.IntegerField (choices=GROUP, verbose_name="Jenis Gudang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Jenis Satuan",blank=True)
    capacity_warehouse = models.IntegerField (max_length=20, verbose_name="Kapasitas Gudang")
    available_capacity_warehouse = models.IntegerField (verbose_name="Sisa Kapasitas Gudang")
#    status = models.BooleanField (verbose_name="Di Setujui",help_text='Jangan di centang apabila masih belum dapat Persetujuan dari Kepala Gudang')
    class Meta:
        verbose_name_plural= _('Master Gudang Produksi')
        verbose_name= _('Master Gudang Produksi')

    def descriptionx(self):
        return '%s' % self.description
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Deskripsi'

    def __unicode__(self):
        return u'%(code)s | %(name)s' % { 'code':self.code_warehouse,'name':self.warehouse_name}


class in_commodity (models.Model):
    departemen_appelant = models.ForeignKey (Department, verbose_name="Departemen Pemohon")
    warehouse = models.ForeignKey (Warehouse, verbose_name="Nama Gudang")
    name_item = models.CharField (max_length=50, verbose_name="Nama Barang")
    type = models.ForeignKey (type_commodity , verbose_name="Jenis Barang")
    quantity_commodity = models.ForeignKey (quantity_commodity, verbose_name="Kualitas Barang")
    date = models.DateTimeField (max_length=20, verbose_name="Tanggal Masuk", blank=True)
    satuan = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_item = models.IntegerField (max_length=20, verbose_name="Jumlah Barang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)

    class Meta:
        verbose_name_plural= _('Penerimaan Surat Permintaan Barang Product Masuk')
        verbose_name= _('Penerimaan Surat Permintaan Barang Product Masuk')

    def descriptionz(self):
        return '%s' % self.description
    descriptionz.allow_tags = True
    descriptionz.short_description = 'Deskripsi'

    def __unicode__(self):
        return u'%s' % self.id


class out_commodity (models.Model):
    departemen_appelant = models.ForeignKey (Department, verbose_name="Departemen Pemohon")
    warehouse = models.ForeignKey(Warehouse, verbose_name="Nama Gudang")
    name_item = models.CharField (max_length=50, verbose_name="Nama Barang")
    type = models.ForeignKey (type_commodity, verbose_name="Jenis Barang")
    quantity_commodity = models.ForeignKey (quantity_commodity, verbose_name="Kualitas Barang")
    date = models.DateTimeField (max_length=20, verbose_name="Tanggal Keluar", blank=True)
    satuan = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_item = models.IntegerField (max_length=20, verbose_name="Jumlah Barang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)

    class Meta:
        verbose_name_plural= _('Penerimaan Surat Permintaan Barang Product Keluar')
        verbose_name= _('Penerimaan Surat Permintaan Barang Product Keluar')

    def descriptionc(self):
        return '%s' % self.description
    descriptionc.allow_tags = True
    descriptionc.short_description = 'Deskripsi'

    def __unicode__(self):
        return u'%s' % self.id

class Warehouse_material(models.Model):
    code_warehouse = models.CharField (max_length=50, verbose_name="Kode Gudang")
    warehouse_name = models.CharField (max_length=50, verbose_name="Nama Gudang")
    type_warehouse = models.IntegerField (choices=GROUP, verbose_name="Jenis Gudang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Jenis Satuan",blank=True)
    capacity_warehouse = models.IntegerField (max_length=20, verbose_name="Kapasitas Gudang")
    available_capacity_warehouse = models.IntegerField (verbose_name="Sisa Kapasitas Gudang")

    class Meta:
        verbose_name_plural= _('Master Gudang Material')
        verbose_name= _('Master Gudang Material')

    def descriptionv(self):
        return '%s' % self.description
    descriptionv.allow_tags = True
    descriptionv.short_description = 'Deskripsi'

    def __unicode__(self):
        return u'%(code)s | %(name)s' % { 'code':self.code_warehouse,'name':self.warehouse_name}

class in_commodity_material (models.Model):
    departemen_appelant = models.ForeignKey (Department, verbose_name="Departemen Pemohon")
    warehouse = models.ForeignKey (Warehouse_material, verbose_name="Nama Gudang")
    name_item = models.CharField (max_length=50, verbose_name="Nama Barang")
    type = models.ForeignKey (type_commodity , verbose_name="Jenis Barang")
    quantity_commodity = models.ForeignKey (quantity_commodity, verbose_name="Kualitas Barang")
    date = models.DateTimeField (max_length=20, verbose_name="Tanggal Masuk", blank=True)
    satuan = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_item = models.IntegerField (max_length=20, verbose_name="Jumlah Barang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)

    class Meta:
        verbose_name_plural= _('Penerimaan Surat Permintaan Barang Material Masuk')
        verbose_name= _('Penerimaan Surat Permintaan Barang Material Masuk')

    def descript(self):
        return '%s' % self.description
    descript.allow_tags = True
    descript.short_description = 'Deskripsi'

    def __unicode__(self):
        return u'%s' % self.id


class out_commodity_material (models.Model):
    departemen_appelant = models.ForeignKey (Department, verbose_name="Departemen Pemohon")
    warehouse = models.ForeignKey(Warehouse_material, verbose_name="Nama Gudang")
    name_item = models.CharField (max_length=50, verbose_name="Nama Barang")
    type = models.ForeignKey (type_commodity, verbose_name="Jenis Barang")
    quantity_commodity = models.ForeignKey (quantity_commodity, verbose_name="Kualitas Barang")
    date = models.DateTimeField (max_length=20, verbose_name="Tanggal Keluar", blank=True)
    satuan = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_item = models.IntegerField (max_length=20, verbose_name="Jumlah Barang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)

    class Meta:
        verbose_name_plural= _('Penerimaan Surat Permintaan Barang Material Keluar')
        verbose_name= _('Penerimaan Surat Permintaan Barang Material Keluar')

    def descrip(self):
        return '%s' % self.description
    descrip.allow_tags = True
    descrip.short_description = 'Deskripsi'

    def __unicode__(self):
        return u'%s' % self.id
