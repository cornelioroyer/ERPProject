from django.db import models
from django.utils.translation import ugettext as _
from Apps.Manufacturing.const import *
#from Apps.Manufacturing.Manufacturing.models import Manufacturing_Order
#from Apps.Manufacturing.Manufacturing.models import *
#from Apps.Manufacturing.ProductionExecution.models import *
from Apps.Manufacturing.ProductionPlanning.models import *
from PIL import Image
from tinymce.models import HTMLField


class Master_Material(models.Model):
    Material_Name = models.CharField(verbose_name=_('Nama'), max_length=30) # Nama = Warna Cat
    Material_Type = models.IntegerField(verbose_name=_('Tipe'), choices=Jenis_Material)
    Description_Material = HTMLField(verbose_name=_('Digunakan'), default='untuk material')
    Material_Quantity = models.DecimalField(verbose_name=_('Jumlah'), max_digits=10, default=0.00, decimal_places=2)
    Unit_Measure = models.ForeignKey('Unit_Of_Measure', verbose_name=_('Satuan'))

    class Meta:
        verbose_name="Material" #
        verbose_name_plural="Material" # berisi material yang terhubung pada inventory

    def material_reviewx(self):
        return '%s' % self.Description_Material
    material_reviewx.allow_tags = True
    material_reviewx.short_description ='Digunakan'

    def __unicode__(self):
        return u'%s' % self.Material_Name
"""    
class Master_BoM (models.Model):											
	BoM = models.CharField(verbose_name=_('Kode BoM'), default='BoM', max_length=6)
	ManufacturingOrder = models.ForeignKey(Manufacturing_Order, verbose_name='Manufacturing Order')
	Add_Date = models.DateField(verbose_name=_('Tanggal Pembuatan'), auto_now_add=True)
			
	class Meta:
		verbose_name="Master BoM"
		verbose_name_plural="Master BoM"
        
	def __unicode__(self):
		return u'%s' % self.BoM
"""


class Unit_Of_Measure(models.Model):
    Unit_of_Measure_Detail = models.CharField(verbose_name='Nama Satuan', max_length=20, )
    Description_Unit = HTMLField(verbose_name=_('Penggunaan'), default='Digunakan sebagai satuan')
    class Meta:
        verbose_name = 'Satuan'
        verbose_name_plural = 'Satuan'	# massa= gram;Ton || volume= ml;liter || heigth/diameter= cm
        ordering = ['id']

    def UnitOfMeasure_reviewx(self):
        return '%s' % self.Description_Unit
    UnitOfMeasure_reviewx.allow_tags = True
    UnitOfMeasure_reviewx.short_description ='Penggunaan'

    def __unicode__(self):
        return u'%s' % self.Unit_of_Measure_Detail
"""		
class Carton(models.Model):
#	Carton_Id = models.CharField(verbose_name=_('Kode'), default='K', max_length=4)
	Carton_Type = models.CharField(verbose_name=_('Tipe'), max_length=25) 
	Carton_Quantity = models.IntegerField(verbose_name=_('Jumlah'), default=0)
	Add_Time_Date = models.DateTimeField(verbose_name=_('Tanggal/Jam'), auto_now_add=True)
	
	class Meta:
		verbose_name="Karton"
		verbose_name_plural="Karton"
	def __unicode__(self):
		return self.Carton_Type
"""
class Master_Team(models.Model):
    Team_Name = models.CharField(verbose_name=_('Tim'), max_length=30, choices=TIM) # = Production || ACL
    Initial_Team = models.CharField(verbose_name=_('Regu'), max_length=5, choices=Initial) # =A, B, C, D, E, F, G, H
    Description_Team = HTMLField(verbose_name=_('Bertugas'), default='Melakukan')
    #	Material_Name = models.CharField(verbose_name=_('Nama'), max_length=15)
    #	Material_Type = models.IntegerField(verbose_name=_('Tipe'), choices=Jenis_Material)
    #	Material_Quantity = models.IntegerField(verbose_name=_('Jumlah')) #

    class Meta:
        verbose_name="Team"
        verbose_name_plural="Team"

    def descriptionx(self):
        return '%s' % self.Description_Team
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Bertugas'

    def __unicode__(self):
        return u'%s' % self.Initial_Team

"""		
class Bill_Of_Material (models.Model):
	#BoM_Id = models.IntegerField(verbose_name=_('Kode Komposisi'))
	Master_BoM = models.ForeignKey(Master_BoM, verbose_name=_('Master BoM'))
	Master_Material = models.ForeignKey(Master_Material, verbose_name=_('Material')) # ||===)> Isi Material=Item
	Material_Quantity = models.DecimalField(verbose_name=_('Jumlah'), max_digits=10, default=0.00, decimal_places=2)
	#DecimalField(verbose_name=_(''), max_digits=10, default=0.00, decimal_places=2)
	Unit_Measure = models.ForeignKey('Unit_Of_Measure', verbose_name=_('Satuan'))
	# Total_Quantity === nanti kasih Dev
	
	class Meta: 
		verbose_name="Bill Of Material"
		verbose_name_plural="2.Bill Of Material"
        
	def __unicode__(self):
		return u'%s' % self.Master_BoM
"""


class rkap_production (models.Model):		# RAK PRODUCTION (rencana kapasitas & jadwal)
    no_reg = models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    speed_in = models.IntegerField(verbose_name=_('Speed')) #
    eff_in	= models.DecimalField(verbose_name=_('Efficiency'), max_digits=5, default=0.00, decimal_places=2) #
    order_in = models.IntegerField(verbose_name=_('Baik'), default=0) #rencana jumlah produk BAIK yang dihasilkan
    #broken_in = models.IntegerField(verbose_name=_('GAGAL'), default=0) #jumlah produk GAGAL yang dihasilkan
    weight_in = models.DecimalField(verbose_name=_('Berat'), max_digits=5, default=0.00, decimal_places=2) #berat produk hasil produksi
    add_date_time = models.DateTimeField(verbose_name=_('Tanggal/Jam')) #tanggal dibuat || waktu (07:00 - 07:00)=24 jam


    class Meta:
        verbose_name="Target"
        verbose_name_plural="Target"

    def incstring(self):
        try:
            data = rkap_production.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'R/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(rkap_production, self).save()

    def __unicode__(self):
        return u'%s' % self.no_reg

class Production_Mechine(models.Model):
    #Mechine_Id = models.
    MC_Production = models.CharField(verbose_name=_('M/C'), max_length=35, help_text='Mesin Produksi Botol', choices=Dapur) # G.1.=[1; 2; 3] D.G || G.2.=[1; 2; 3] D.G
    Acl_Production = models.CharField(verbose_name=_('ACL'), max_length=10, help_text='Mesin Pelabelan Botol', choices=ACL) # =ACL-[1; 2; 3; 4]
    Forklift_Quantity = models.IntegerField(verbose_name=_('Forklift'), default=0)
    BlowTorch_Quantity = models.IntegerField(verbose_name=_('Blow Torch'), default=0)
    #M_C = models.CharField(verbose_name=_('M/C'),)
    Current_Status = models.IntegerField(verbose_name=_('Status'), choices=Status_Dapur) #PRODUKSI || STOP PRODUKSI


    class Meta:
        verbose_name="Workcenter"
        verbose_name_plural="Workcenter"

    def __unicode__(self):
        return u'%s' % self.MC_Production

class ProductLabel(models.Model):          # <=> Specifation Product
    no_reg = models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    Product_Label = models.ImageField(verbose_name=_('Label'), upload_to='uploads/logo', blank=True, default='uploads/default.jpg')
    Description_Label = HTMLField(verbose_name=_('Keterangan'), default='gambar desain label botol')

    def display_image(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="75"/>' % (settings.MEDIA_URL, self.Product_Label)

    display_image.short_description = 'Gambar'
    display_image.allow_tags = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.Product_Label:
            return

        Product_Label  = Image.open(self.Product_Label)
        (width, height) = Product_Label.size
        size = (110,110)
        Product_Label = Product_Label.resize(size, Image.ANTIALIAS)
        Product_Label.save(self.Product_Label.path)
        super(ProductLabel, self).save()
    def incstring(self):
        try:
            data = ProductLabel.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[1])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'L/%(unik)s' % {'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(ProductLabel, self).save()

    class Meta:
        verbose_name="Label"
        verbose_name_plural="Label"

    def descriptionx(self):
        return '%s' % self.Description_Label
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Keterangan'

    def __unicode__(self):
        return u'%s' % self.no_reg


class ProductDesign(models.Model):          # <=> Specifation Product
    no_reg = models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    Product_Design = models.ImageField(verbose_name=_('Design'), upload_to='uploads/logo', blank=True, default='uploads/default.jpg')
    Description_Design = HTMLField(verbose_name=_('Keterangan'), default='gambar desain mould botol')

    def display_image(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="75"/>' % (settings.MEDIA_URL, self.Product_Design)

    display_image.short_description = 'Gambar'
    display_image.allow_tags = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.Product_Design:
            return

        Product_Design  = Image.open(self.Product_Design)
        (width, height) = Product_Design.size
        size = (110,110)
        Product_Design = Product_Design.resize(size, Image.ANTIALIAS)
        Product_Design.save(self.Product_Design.path)
        super(ProductDesign, self).save()
    def incstring(self):
        try:
            data = ProductDesign.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[1])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'Ds/%(unik)s' % {'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(ProductDesign, self).save()
    class Meta:
        verbose_name="Design"
        verbose_name_plural="Design"

    def descriptionx(self):
        return '%s' % self.Description_Design
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Keterangan'

    def __unicode__(self):
        return u'%s' % self.no_reg


class Product_Dimension_Diameter(models.Model):
    no_reg	= models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    Diam_fd1 = models.DecimalField(verbose_name=_('Diameter Finish D1'), max_digits=10, default=0.00, decimal_places=2)#Diameter Finish D1
    Diam_fd2 = models.DecimalField(verbose_name=_('Diameter Finish D2'), max_digits=10, default=0.00, decimal_places=2)
    Diam_fd3 = models.DecimalField(verbose_name=_('Diameter Finish D3'), max_digits=10, default=0.00, decimal_places=2)
    Diam_bd4 = models.DecimalField(verbose_name=_('Diameter Bore D4'), max_digits=10, default=0.00, decimal_places=2)#Diameter Bore D4
    Diam_fd5 = models.DecimalField(verbose_name=_('Diameter Finish D5'), max_digits=10, default=0.00, decimal_places=2)
    Diam_body_pinch = models.DecimalField(verbose_name=_('Diameter Body Pinch'), max_digits=10, default=0.00, decimal_places=2)
    Diam_body_sh_s = models.DecimalField(verbose_name=_('Diameter Body SH/S'), max_digits=10, default=0.00, decimal_places=2)
    Description_Diameter = HTMLField(verbose_name=_('Keterangan'), default='desain diameter botol')
    Inspection_Products = models.IntegerField(verbose_name=_('Status'), choices=Inspect)

    class Meta:
        verbose_name="Diameter"
        verbose_name_plural="Diameter"

    def descriptionx(self):
        return '%s' % self.Description_Diameter
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Keterangan'

    def incstring(self):
        try:
            data = Product_Dimension_Diameter.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[1])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'Da/%(unik)s' % {'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Product_Dimension_Diameter, self).save()
    def __unicode__(self):
        return u'%s' % self.no_reg


class Product_Dimension_Height (models.Model):
    no_reg = models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    Height_h = models.DecimalField(verbose_name=_('Height H'), max_digits=10, default=0.00, decimal_places=2)
    Height_fh = models.DecimalField(verbose_name=_('Height Finish H'), max_digits=10, default=0.00, decimal_places=2)
    Ovality_Body = models.DecimalField(verbose_name=_('Ovality Body'), max_digits=10, default=0.00, decimal_places=2)
    Ovality_Finish_Ring = models.DecimalField(verbose_name=_('Ovality Finish Ring'), max_digits=10, default=0.00, decimal_places=2)
    Description_Height = HTMLField(verbose_name=_('Keterangan'), default='desain tinggi botol')
    Inspection_Products = models.IntegerField(verbose_name=_('Status'), choices=Inspect)
    #	Product_Design = models.ImageField(verbose_name=_('Design'), upload_to='uploads/logo', blank=True, default='uploads/default.jpg')


    class Meta:
        verbose_name="Tinggi"
        verbose_name_plural="Tinggi"

    def descriptionx(self):
        return '%s' % self.Description_Height
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Keterangan'

    def incstring(self):
        try:
            data = Product_Dimension_Height.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[1])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'H/%(unik)s' % {'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Product_Dimension_Height, self).save()
    def __unicode__(self):
        return u'%s' % self.no_reg


class Product_Volume (models.Model):          # <=> Specifation Product
    no_reg = models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    Bf_Capacity = models.DecimalField(verbose_name=_('Bf Capacity'), max_digits=10, default=0.00, decimal_places=2)
    Fill_Capacity = models.DecimalField(verbose_name=_('Fill Capacity'), max_digits=10, default=0.00, decimal_places=2)
    Fill_Point_From_Top = models.DecimalField(verbose_name=_('Fill Point From Top'), max_digits=10, default=0.00, decimal_places=2)
    Weight = models.DecimalField(verbose_name=_('Berat'), max_digits=10, default=0.00, decimal_places=2)
    Description_Volume = HTMLField(verbose_name=_('Keterangan'), default='desain volume botol')
    Inspection_Products = models.IntegerField(verbose_name=_('Status'), choices=Inspect)

    class Meta:
        verbose_name="Volume"
        verbose_name_plural="Volume"

    def descriptionx(self):
        return '%s' % self.Description_Volume
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Keterangan'

    def incstring(self):
        try:
            data = Product_Volume.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[1])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'V/%(unik)s' % {'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Product_Volume, self).save()
    def __unicode__(self):
        return u'%s' % self.no_reg


class Product_Physics (models.Model):		# ||===============================>> DATA Fisik DIPEROLEH SETELAH TES LAB DILAKUKAN
    no_reg = models.CharField(verbose_name=_('Kode'), max_length=20, editable=False)
    Thermal_Shock = models.DecimalField(verbose_name=_('Thermal Shock'), max_digits=10, default=0.00, decimal_places=2)
    Wavy_Finish = models.DecimalField(verbose_name=_('Wavy Finish'), max_digits=10, default=0.00, decimal_places=2)
    Sunken_BP = models.DecimalField(verbose_name=_('Sunken Body/Panel'), max_digits=10, default=0.00, decimal_places=2)
    Sloping_Finish = models.DecimalField(verbose_name=_('Sloping Finish'), max_digits=10, default=0.00, decimal_places=2)
    Internal_Pressure = models.DecimalField(verbose_name=_('Internal Pressure'), max_digits=10, default=0.00, decimal_places=2)
    Contact_Point = models.DecimalField(verbose_name=_('Contact Point'), max_digits=10, default=0.00, decimal_places=2)
    Bottom_PUp = models.DecimalField(verbose_name=_('Bottom Push Up'), max_digits=10, default=0.00, decimal_places=2)
    Body_PDS = models.DecimalField(verbose_name=_('Body/Panel/DS'), max_digits=10, default=0.00, decimal_places=2)
    Bearing_Surface = models.DecimalField(verbose_name=_('Bearing Surface'), max_digits=10, default=0.00, decimal_places=2)
    Annealing_Cord = models.DecimalField(verbose_name=_('Annealing/Cord'), max_digits=10, default=0.00, decimal_places=2)
    Des_Physics = HTMLField(verbose_name=_('Keterangan'), default='desain fisik botol')
    Inspection_Products = models.IntegerField(verbose_name=_('Status'), choices=Inspect)

    class Meta:
        verbose_name="Fisik"
        verbose_name_plural="Fisik"

    def descriptionx(self):
        return '%s' % self.Des_Physics
    descriptionx.allow_tags = True
    descriptionx.short_description = 'Keterangan'


    def incstring(self):
        try:
            data = Product_Physics.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[1])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'F/%(unik)s' % {'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Product_Physics, self).save()
    def __unicode__(self):
        return u'%s' % self.no_reg

"""		
class ACL_Mechine (models.Model):
	Acl_Production = models.CharField(verbose_name=_('ACL'), max_length=10, choices=ACL) # =ACL-[1; 2; 3; 4]
	Current_Status = models.IntegerField(verbose_name=_('Status'), choices=Status_ACL) #PRODUKSI || STOP PRODUKSI
	
	class Meta:
		verbose_name="Mesin ACL"
		verbose_name_plural="3.Mesin ACL"
		
	def __unicode__(self):
		return u'%s' % self.Acl_Production
"""


#Create your models here.
