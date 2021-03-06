from django.db import models
from django.utils.translation import ugettext as _
from Apps.Inventory.Property_Inv.models import quantity_commodity, type_commodity, Jenis_satuan
from Apps.Inventory.Inventory_Planing.models import Warehouse, Warehouse_material
from Apps.Inventory.Inventory_Handling.models import *
from tinymce.models import HTMLField
from django.db.models.signals import post_save

class Control_warehouse (models.Model):
    warehouse_name = models.ForeignKey (Warehouse, verbose_name="Nama Gudang")
    commodity = models.ForeignKey ("Inventory_Handling.Ms_commodity", verbose_name="Nama Barang")
    category = models.ForeignKey (quantity_commodity, verbose_name="Kualitas Barang")
    date = models.DateTimeField (max_length=20, verbose_name="Tanggal", blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_commodity = models.IntegerField (max_length=20, verbose_name="Jumlah Barang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)
    
    
    class Meta:
        verbose_name_plural= _('Control Gudang Produksi')
        verbose_name= _('Control Gudang Produksi')
        
        
    def __unicode__(self):
        return u'%s' % self.id
    

class needs_commodity (models.Model):
    number_needs = models.CharField (max_length=20, verbose_name="Nomer Kebutuhan",blank=True)
    name_commodity = models.CharField (max_length=50, verbose_name="Nama Barang")
    commodity_code = models.ForeignKey ("Inventory_Handling.master_commodity", verbose_name="Kode Barang",blank=True)
    date = models.DateField (max_length=20, verbose_name="Tanggal",blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_request = models.IntegerField (max_length=20, verbose_name="Jumlah Permintaan")
    stock = models.IntegerField (max_length=20, verbose_name="Stock",blank=True)
    total_purchase = models.IntegerField (max_length=20, verbose_name="Jumlah Pembelian",blank=True)
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)
    
    class Meta:
        verbose_name_plural= _('Permintaan Kebutuhan Barang Material')
        verbose_name= _('Permintaan Kebutuhan Barang Material') 
        
        
    def __unicode__(self):
        return u'%s' % self.id 


class Control_warehouse_material (models.Model):
    warehouse_name = models.ForeignKey (Warehouse_material, verbose_name="Nama Gudang")
    commodity = models.ForeignKey ("Inventory_Handling.master_commodity", verbose_name="Nama Barang")
    category = models.ForeignKey (quantity_commodity, verbose_name="Kualitas Barang")
    date = models.DateTimeField (max_length=20, verbose_name="Tanggal", blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_commodity = models.IntegerField (max_length=20, verbose_name="Jumlah Barang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)
    
    
    class Meta:
        verbose_name_plural= _('Control Gudang Material')
        verbose_name= _('Control Gudang material')
        
        
    def __unicode__(self):
        return u'%s' % self.id
