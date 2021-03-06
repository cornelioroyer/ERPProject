from django.contrib import admin
from Apps.Asset.Penjualan.models import *
from django.contrib.auth.models import Group

class DataDirectInline(admin.TabularInline):
    model = Direct
    extra = 1
    max_num = 0
    can_delete = True

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'staff':
            if getattr(obj, 'sale', None) == None:
                readonly_fields = ('sale','customer_name','detail_sale','total_price','sale_add_date','payment_method','detail_payment','faktur',)
            else :
                readonly_fields += ()

            if getattr(obj, 'header_disposal', None) != None:
                readonly_fields = ('sale','detail_sale','total_price','sale_add_date','payment_method','detail_payment')
        else :
            readonly_fields = ('sale','detail_sale','total_price','sale_add_date','payment_method','detail_payment',)

        return readonly_fields

class DataProcInline(admin.TabularInline):
    model = Procurement
    extra = 1
    max_num = 0
    exclude = ['detail_payment','detail_sale','total_price','published','slug','image','payment_method',]
    can_delete = True


    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'staff':
            if getattr(obj, 'sale', None) == None:
                readonly_fields = ('no_reg','sale','title','harga_awal','sale_add_date','end_enlisting','end_bid','winner','harga_deal','faktur',)
            else :
                readonly_fields += ()
        else :
            readonly_fields = ('no_reg','sale','title','harga_awal','sale_add_date','end_enlisting','end_bid','payment_method','winner','harga_deal',)

        return readonly_fields
        #readonly_fields= ('no_reg','sale','title','harga_total','end_enlisting','sale_add_date','end_bid','payment_method','winner','status','published',)


class Sale_admin(admin.ModelAdmin):
    list_display = ['no_reg','asset','method_sale']
    search_fields = ['no_reg','asset','method_sale']
    inlines = [DataProcInline,DataDirectInline]
    list_filter = ['method_sale',]


    def get_form(self, request, obj=None, **kwargs):
        data = Group.objects.get(user=request.user)
        form = super(Sale_admin, self).get_form(request, obj, **kwargs)
        if data.name == 'staff':
            form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(usage_status=2)
        return form


admin.site.register(Sale, Sale_admin)

class DataCusProcInline(admin.TabularInline):
    model = Customer_proc
    extra = 1
    max_num = 0
    can_delete = True
    readonly_fields = ['ID','procurement','add_date','customer','bid_value',]

class Procurement_admin(admin.ModelAdmin):
    list_display = ['no_reg','sale','title','harga_awal','end_enlisting','sale_add_date','end_bid','winner','harga_deal','status','faktur','published','display_image',]
    search_fields = ['title','published']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [DataCusProcInline,]
    list_filter = ['sale_add_date','payment_method',]
    list_editable = ['published',]

    def suit_row_attributes(self, obj, request):
        css_class = {
            True: 'success', False: 'error',}.get(obj.published)
        if css_class:
            return {'class': css_class, 'data': obj.published}

    def get_form(self, request, obj=None, **kwargs):
        data = Group.objects.get(user=request.user)
        form = super(Procurement_admin, self).get_form(request, obj, **kwargs)
        if data.name == 'staff':
            if getattr(obj, 'sale', None) == None:
                form.base_fields['sale'].queryset = form.base_fields['sale'].queryset.filter(method_sale=2)
            else:
                self.exclude = ['detail_sale',]
        return form

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'unit':
            readonly_fields = ('no_reg','sale','title','end_enlisting','sale_add_date','end_bid','payment_method','winner','harga_deal','status','published')
        elif data.name == 'staff':
            readonly_fields = ()
            if getattr(obj, 'sale', None) != None:
                readonly_fields = ('no_reg','sale','end_enlisting','sale_add_date','total_price','detail_salex','end_bid','winner','harga_deal','status','published',)
            else:
                readonly_fields += ('payment_method','detail_payment',)
            if getattr(obj,'payment_method', None) != True:
                readonly_fields += ()

        return readonly_fields

admin.site.register(Procurement, Procurement_admin)


class DataBiddingInline(admin.TabularInline):
    model = Bidding
    extra = 1
    can_delete = True
    fields = ('msg','uname','msg_add_date',)
    readonly_fields = ('uname','msg_add_date',)

class Customer_proc_admin(admin.ModelAdmin):
    list_display = ['ID','procurement','add_date','customer','nilai_penawaran']
    search_fields = ['procurement']
    inlines = [DataBiddingInline,]

#	def get_form(self, request, obj=None, **kwargs):
#		data = Group.objects.get(user=request.user)
#		form = super(Customer_proc_admin, self).get_form(request, obj, **kwargs)
#		if data.name == 'staff':
#			form.base_fields['procurement'].queryset = form.base_fields['procurement'].queryset.filter(status='Penawaran Dibuka')
#		return form

admin.site.register(Customer_proc, Customer_proc_admin)


class Bidding_Admin(admin.ModelAdmin):
    list_display = [ 'custom_proc','msg_add_date','uname','msg']
admin.site.register(Bidding, Bidding_Admin)

class Direct_admin(admin.ModelAdmin):
    list_display = ['sale','customer_name','detail_salex','sale_add_date','payment_method','harga_total','detail_paymentx',]
    search_fields = ['asset','payment_method']

    def get_form(self, request, obj=None, **kwargs):
        data = Group.objects.get(user=request.user)
        form = super(Direct_admin, self).get_form(request, obj, **kwargs)
        if data.name == 'staff':
            if getattr(obj, 'sale', None) == None:
                form.base_fields['sale'].queryset = form.base_fields['sale'].queryset.filter(method_sale=1)
            else:
                self.exclude = ['detail_sale','detail_payment',]
        return form

    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'unit':
            readonly_fields = ('sale','detail_salex','total_price','sale_add_date','payment_method','detail_paymentx',)

        elif data.name == 'staff':
            if getattr(obj, 'sale', None) != None:
                readonly_fields = ('sale','detail_salex','total_price','sale_add_date','payment_method','detail_paymentx','customer_name',)
            else :
                readonly_fields += ()

            if getattr(obj, 'header_disposal', None) != None:
                readonly_fields = ('sale','detail_salex','total_price','sale_add_date','payment_method','detail_paymentx')
        else :
            readonly_fields = ()

        return readonly_fields

admin.site.register(Direct, Direct_admin)

class Tr_Asset_Sale_Invoice_admin(admin.ModelAdmin):
    list_display = ['no_reg','customer','date','total','info',]
    search_fields = ['date',]
    inlines = [DataProcInline,DataDirectInline]

admin.site.register(Tr_Asset_Sale_Invoice, Tr_Asset_Sale_Invoice_admin)
