"""Develop By - Achmad Afiffudin N"""

from django.contrib import admin
from Apps.Accounting.AccountReceivable.models import *
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import HttpResponse
#from Apps.Distribution.FromSales.models import *
from django.db.models import signals
from django.contrib.auth.models import *
from Apps.Distribution.invoice.models import *
from suit.widgets import *

class ItemInline(admin.StackedInline):
    model = DetailFaktur
    extra = 1
    verbose_name_plural = 'Detail Order Item'
    can_delete = False
    fieldsets = [
        (None, {
            'fields': ['color', 'category', ('weight', 'capacity'), ('height', 'diameter'), 'image', 'label', 'quantity'
            , 'price']
        })
    ]

    def get_formset(self, request, obj=None):
        formset = super(ItemInline, self).get_formset(request, obj)

        if obj is not None and obj.status in (INVOICE_FINISH_STATUS):
            formset.max_num = 0
            formset.can_delete = False
        if obj is not None:
            formset.extra = 0
        return formset

    def get_readonly_fields(self, request, obj=None):
        readonly = super(ItemInline, self).get_readonly_fields(request, obj)
        readonly = ('color', 'category', 'capacity', 'height', 'weight', 'diameter', 'image', 'label', 'quantity', 'price')
        return readonly

class Detail_Sales_AccountInline(admin.TabularInline):
    model = Detail_Sales_Account
    can_delete = False
    verbose_name_plural = 'Detail Akun Faktur'
    list_per_page  = 2
    max_num = 2
    fields = ['Invoice','Account','Type',]

class Sales_InvoiceAdmin(admin.ModelAdmin):
    list_display = ['number', 'tax', 'payment_term', 'payment_type', 'shipping_methods', 'sales_person',]
    list_filter = ['payment_term', 'payment_type', 'shipping_methods', 'status']
    date_hierarchy = 'date'
    readonly_fields= ('number', 'so_reff','customer','sales_person','status','date','po_reference','currency','tax', 'payment_term', 'payment_type','ship_address','payment_type','term_service','shipping_methods', 'sales_person','quotation','sales_type','total',)    
    search_fields = ['number', 'customer']
    inlines = [ItemInline, Detail_Sales_AccountInline]

    def suit_row_attributes(self, obj, request):
		css_class = {
			'Akun Terisi': 'success','Akun Tidak Lengkap': 'warning', 'Akun Kosong': 'error'}.get(obj.sts())
		if css_class:
			return {'class': css_class, 'data': obj.sts()}

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def queryset(self, request):
        if request.user.is_superuser:
            return Sales_Invoice.objects.filter(Q(status=1) | Q(status=2) | Q(status=3) | Q(status=4))
        else:
            return Sales_Invoice.objects.filter(Q(status=3) | Q(status=4))

admin.site.register(Sales_Invoice, Sales_InvoiceAdmin)

class FormSL(forms.ModelForm):
    class Meta:
        widgets = {
            'Bank_Payment': LinkedSelect(attrs={'class': 'input-large'}),
            'Cash_Payment': LinkedSelect(attrs={'class': 'input-large'}),
            'Memo' : Textarea(attrs={'rows': '3'}),
            'Date': SuitDateWidget
        }

class Tr_Sales_PaymentInline(admin.StackedInline):
    model = Tr_Sales_Payment
    form = FormSL
    can_delete = False
    verbose_name_plural = 'Pembayaran'
    list_per_page  = 5
    max_num = 5
    extra = 1
    fields = ['Paid_Amount','Bank_Payment','Cash_Payment','Date','Memo','Control',]

class Tr_Sales_ReceiptAdmin(admin.ModelAdmin):   
    list_display = ('Invoice','total_payment','total_residu','total_credit','payment_status',)
    #list_filter = ('Invoice__Date',)
    #ordering = ('Invoice__Date', )
    search_fields = ('Invoice',)
    exclude = ('Total_Payment','Total_Residu','Total_Credit','Payment_Status',)
    inlines = [Tr_Sales_PaymentInline,]
    
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('Invoice','total_payment','total_residu','total_credit','payment_status',)
        return self.readonly_fields

    def suit_row_attributes(self, obj, request):
		css_class = {
			'Lunas': 'success','Kredit': 'warning','Belum Dibayar': 'error',}.get(obj.payment_status())
		if css_class:
			return {'class': css_class, 'data': obj.payment_status()}

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
    
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
admin.site.register(Tr_Sales_Receipt, Tr_Sales_ReceiptAdmin)

class Detail_Sales_Payment_AccountInline(admin.TabularInline):
    model = Detail_Sales_Payment_Account
    can_delete = False
    verbose_name_plural = 'Jurnal Item'
    list_per_page  = 2
    max_num = 2
    fields = ['Payment','Account','Type',]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'staf_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Payment','Account','Type',)
        return readonly_fields

class Tr_Sales_PaymentAdmin(admin.ModelAdmin):   
    list_display = ('Payment_No','Paid_Amount','Date','Memo','status',)
    list_filter = ('Payment_No','Paid_Amount',)
    date_hierarchy = 'Date'    
    ordering = ('-id', )
    search_fields = ('Payment_No',)
    readonly_fields = ('Payment_No','Invoice','Paid_Amount','Date','Bank_Payment','Cash_Payment',
    'Memo','Period','Journal','Control')
    inlines = [Detail_Sales_Payment_AccountInline,]

    fieldsets = [(None, {
        'fields': ['Payment_No','Invoice','Date','Period','Journal','Memo','Paid_Amount']
    })]

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def suit_row_attributes(self, obj, request):
		css_class = {
			'Akun Terisi': 'success','Akun Tidak Lengkap': 'warning', 'Akun Kosong': 'error'}.get(obj.status())
		if css_class:
			return {'class': css_class, 'data': obj.status()}

admin.site.register(Tr_Sales_Payment, Tr_Sales_PaymentAdmin)

#Retur
class Detail_Return_AccountInline(admin.TabularInline):
    model = Detail_Return_Account
    can_delete = False
    verbose_name_plural = 'Jurnal Item'
    list_per_page  = 10
    max_num = 2
    fields = ['Return','Account','Type',]

class Detail_ReturnInline(admin.TabularInline):
    model = Detail_Sales_Return
    verbose_name_plural = 'Detail Retur'
    list_per_page  = 10
    max_num = 2
    extra = 1
    fields = ['Item', 'Quantity', 'Price',]

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('Item', 'Quantity', 'Price',)
        return self.readonly_fields
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class Sales_ReturnAdmin(admin.ModelAdmin):   
    list_display = ('Sales_Return_No','Invoice','Date','Currency','Memo','total','status',)
    list_filter = ('Invoice',)
    ordering = ('-Date', )
    date_hierarchy = 'Date'
    search_fields = ('Sales_Return_No',)
    readonly_field= ('Invoice',)
    exclude = ('Total','Period',)
    inlines = [Detail_ReturnInline, Detail_Return_AccountInline,]

    def has_add_permission(self, request, obj=None):
        return False  

    def suit_row_attributes(self, obj, request):
		css_class = {
			'Akun Kosong': 'error','Akun Terisi': 'success',}.get(obj.status())
		if css_class:
			return {'class': css_class, 'data': obj.status()}

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('Sales_Return_No','Invoice','Memo','Date','Currency','Period','Journal','total',)
        return self.readonly_fields

admin.site.register(Sales_Return, Sales_ReturnAdmin)

class DirectInline(admin.TabularInline):
    model = Direct
    verbose_name_plural = 'Detail Penjualan Langsung'
    extra = 1
    max_num = 0
    can_delete = False
    fields=('sale','customer_name', 'sale_add_date','total_price',)
    readonly_fields =('sale','customer_name', 'sale_add_date','total_price',)

class ProcInline(admin.TabularInline):
    model = Procurement
    verbose_name_plural = 'Detail Pelelangan'
    extra = 1
    max_num = 0
    exclude = ['detail_payment','detail_sale','total_price','published','slug','image',]
    can_delete = False
    fields=('no_reg','sale','winner','harga_deal',)
    readonly_fields =('no_reg','sale','winner','harga_deal',)

class Detail_Asset_Sale_AccountInline(admin.TabularInline):
    model = Detail_Asset_Sale_Account
    can_delete = False
    verbose_name_plural = 'Detail Akun'
    list_per_page  = 2
    max_num = 2
    fields = ['Invoice','Account','Type',]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'staf_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Invoice','Account','Type',)
        return readonly_fields

class Asset_Sale_InvoiceAdmin(admin.ModelAdmin):   
    list_display = ('no_reg','customer','date','payment_term','tax','total',)
    list_filter = ('date',)
    ordering = ('-date', )
    search_fields = ('no_reg',)
    readonly_fields= ('no_reg','journal','period','customer','date','payment_term','currency','info','tax','total',)
    date_hierarchy = 'date'
    exclude = ('total',)
    inlines = [DirectInline,ProcInline,Detail_Asset_Sale_AccountInline,]

    def suit_row_attributes(self, obj, request):
		css_class = {
			'Akun Terisi': 'success','Akun Tidak Lengkap': 'warning', 'Akun Kosong': 'error'}.get(obj.status())
		if css_class:
			return {'class': css_class, 'data': obj.status()}

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
    
admin.site.register(Asset_Sale_Invoice, Asset_Sale_InvoiceAdmin)

class Tr_Asset_Sale_PaymentInline(admin.StackedInline):
    model = Tr_Asset_Sale_Payment
    can_delete = True
    verbose_name_plural = 'Pembayaran'
    list_per_page  = 0
    max_num = 5
    extra = 1
    fields = ['Paid_Amount','Date','Bank_Payment','Cash_Payment','Memo','Control',]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser:
            readonly_fields = ()
        elif user.name == 'pengendali_keuangan':
            readonly_fields = ('Paid_Amount','Date','Bank_Payment','Cash_Payment','Memo',)
        elif user.name == 'staf_pemasukan':
            readonly_fields = ('Control',)
        else:readonly_fields = ('Paid_Amount','Date','Bank_Payment','Cash_Payment','Memo','Control',)
        return readonly_fields

class Tr_Asset_Sale_ReceiptAdmin(admin.ModelAdmin):   
    list_display = ('Invoice','total_payment','total_residu','total_credit','payment_status',)
    list_filter = ('Invoice',)
    search_fields = ('Invoice',)
    exclude = ('Total_Payment','Total_Residu','Total_Credit','Payment_Status',)
    readonly_fields = ('Invoice','total_payment','total_residu','total_credit','payment_status',)
    inlines = [Tr_Asset_Sale_PaymentInline,]

    def suit_row_attributes(self, obj, request):
		css_class = {
			'Lunas': 'success','Kredit': 'warning','Belum Dibayar': 'error',}.get(obj.payment_status())
		if css_class:
			return {'class': css_class, 'data': obj.payment_status()}

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
    
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False  

admin.site.register(Tr_Asset_Sale_Receipt,Tr_Asset_Sale_ReceiptAdmin)

class Detail_Asset_Sale_Payment_AccountInline(admin.TabularInline):
    model = Detail_Asset_Sale_Payment_Account
    can_delete = False
    verbose_name_plural = 'Detail Akun'
    list_per_page  = 2
    max_num = 2
    extra = 2
    fields = ['Payment','Account','Type',]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'staf_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Payment','Account','Type',)
        return readonly_fields

class Tr_Asset_Sale_PaymentAdmin(admin.ModelAdmin):
    list_display = ('Payment_No','Paid_Amount','Date','Payment_Ref','Memo','status',)
    list_filter = ('Date',)
    date_hierarchy = 'Date'
    ordering = ('-Date', )
    search_fields = ('Payment_No','Payment_Ref',)
    exclude = ('Invoice','Period','Journal',)
    readonly_fields = ('Payment_No','Paid_Amount','Bank_Payment','Cash_Payment','Date','Payment_Ref','Period','Journal','Memo','Control',)
    inlines = [Detail_Asset_Sale_Payment_AccountInline,]

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def suit_row_attributes(self, obj, request):
		css_class = {
			'Akun Terisi': 'success','Akun Tidak Lengkap': 'warning', 'Akun Kosong': 'error'}.get(obj.status())
		if css_class:
			return {'class': css_class, 'data': obj.status()}

admin.site.register(Tr_Asset_Sale_Payment,Tr_Asset_Sale_PaymentAdmin)
