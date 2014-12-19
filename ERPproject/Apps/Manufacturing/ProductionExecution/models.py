from django.db import models
from django.utils.translation import ugettext as _
from Apps.Manufacturing.ProductionExecution.models import *
from Apps.Manufacturing.ProductionPlanning.models import production_plans
from Apps.Manufacturing.ProductionPlanning.models import *
from Apps.Manufacturing.MasterData.models import *
"""	
class out_production (models.Model):
	speed_out = models.DecimalField(verbose_name=_('Speed'), max_digits=5, decimal_places=2) # FORMULANYA LOM TAHU
	eff_out	= models.DecimalField(verbose_name=_('Efficiency'), max_digits=5, decimal_places=2) # FORMULANYA LOM TAHU 
	order_out = models.IntegerField(verbose_name=_('Baik'), default=0) #jumlah produk BAIK yang dihasilkan = order_in + 15% * order_in
	broken_out = models.IntegerField(verbose_name=_('Gagal'), default=0) #jumlah produk GAGAL yang dihasilkan
	weight_out = models.DecimalField(verbose_name=_('Berat'), max_digits=5, decimal_places=2) #berat produk hasil produksi
	add_date_time = models.DateTimeField(verbose_name=_('Tanggal/Jam'), auto_now_add=True) #tanggal dibuat || waktu (07:00 - 07:00)=24 jam
	
	
	class Meta:
		verbose_name="Item Produksi"
		verbose_name_plural="Item Produksi"
        
	def __unicode__(self):
		return u'%s' % self.speed_out
"""	
class production_record (models.Model):
	Production_Plans = models.ForeignKey(production_plans, verbose_name=_('Production Schedule'))
#	Out_Production = models.ForeignKey(out_production, verbose_name=_('Item Produksi'))
	speed_out = models.DecimalField(verbose_name=_('Speed'), max_digits=5, decimal_places=2) # FORMULANYA LOM TAHU
	eff_out	= models.DecimalField(verbose_name=_('Efficiency'), max_digits=5, decimal_places=2) # FORMULANYA LOM TAHU 
	order_out = models.IntegerField(verbose_name=_('Baik'), default=0) #jumlah produk BAIK yang dihasilkan = order_in + 15% * order_in
	broken_out = models.IntegerField(verbose_name=_('Gagal'), default=0) #jumlah produk GAGAL yang dihasilkan
	weight_out = models.DecimalField(verbose_name=_('Berat'), max_digits=5, decimal_places=2) #berat produk hasil produksi
	add_date_time = models.DateTimeField(verbose_name=_('Tanggal/Jam'), auto_now_add=True) #tanggal dibuat || waktu (07:00 - 07:00)=24 jam

	   
	class Meta:
		verbose_name="Receive Products"
		verbose_name_plural="3.Receive Products"
        
	def __unicode__(self):
		return u'%s' % self.id
		
		
class Use_Resources (models.Model):
	Production_Plans = models.ForeignKey(production_plans, verbose_name=_('Production Schedule')) #'Production_Plans','Issue_Material','	Machine_Usage',
	Issue_Material = models.ForeignKey(Bill_Of_Material, verbose_name=_('Issue Material'))
	Machine_Usage = models.ForeignKey(Production_Mechine, verbose_name=_('Mechine Usage'))
	add_date_time = models.DateTimeField(verbose_name=_('Tanggal/Jam'), auto_now_add=True) #tanggal dibuat || waktu (07:00 - 07:00)=24 jam
#	speed_out = models.DecimalField(verbose_name=_('Speed'), max_digits=5, decimal_places=2) # FORMULANYA LOM TAHU
#	eff_out	= models.DecimalField(verbose_name=_('Efficiency'), max_digits=5, decimal_places=2)# FORMULANYA LOM TAHU
#	order_out = models.IntegerField(verbose_name=_('Baik'), default=0) #jumlah produk BAIK yang dihasilkan = order_in + 15% * order_in
#	broken_out = models.IntegerField(verbose_name=_('Gagal'), default=0) #jumlah produk GAGAL yang dihasilkan
#	weight_out = models.DecimalField(verbose_name=_('Berat'), max_digits=5, decimal_places=2) #berat produk hasil produksi
	
	
	
	class Meta:
		verbose_name="Use Resources"
		verbose_name_plural="1.Use Resources"
        
	def __unicode__(self):
		return u'%s' % self.id
		
		
class Inspection_Products (models.Model):
	Production_Plans = models.ForeignKey(production_plans, verbose_name=_('Production Schedule'))
#	Out_Labeling = models.ForeignKey(out_labeling, verbose_name=_('Item Pelabelan'))
	Dimension_Diameter = models.ForeignKey(Product_Dimension_Diameter, verbose_name=_('Diameter')) #'Dimension_Diameter','Dimension_Height','Volume','Physics',
	Dimension_Height = models.ForeignKey(Product_Dimension_Height, verbose_name=_('Tinggi'))
	Volume = models.ForeignKey(Product_Volume, verbose_name=_('Volume'))
	Physics = models.ForeignKey(Product_Physics, verbose_name=_('Fisik'))
	   
	class Meta:
		verbose_name="Inspection Products"
		verbose_name_plural="2.Inspection Products"
        
	def __unicode__(self):
		return u'%s' % self.id
		
#Create your models here.

