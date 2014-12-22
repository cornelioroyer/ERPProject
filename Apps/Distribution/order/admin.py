from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from Apps.Distribution.order.models import SalesOrder, QuoteOrder, RequestOrder, OrderItem
from django import forms
from suit.widgets import EnclosedInput, Select, AutosizedTextarea, SuitDateWidget, SuitSplitDateTimeWidget
from library.const.order import SO_FINISH_STATUS, INVOICE_FINISH_STATUS, DO_FINISH_STATUS
from Apps.Distribution.customer.models import Company
from django_select2 import AutoModelSelect2Field, AutoHeavySelect2Widget
from django.db.models import Q
from django.http import HttpResponseRedirect


class FormItemInline(forms.ModelForm):
    class Meta:
        widgets = {
            'capacity': EnclosedInput(append='ml', attrs={'class': 'input-small'}),
            'height': EnclosedInput(append='mm', attrs={'class': 'input-small'}),
            'quantity': EnclosedInput(attrs={'class': 'input-small'}),
            'price': EnclosedInput(attrs={'class': 'input-large'}),
            'weight': EnclosedInput(append='gr', attrs={'class': 'input-small'}),
            'diameter': EnclosedInput(append='mm', attrs={'class': 'input-small'}),
            'color': Select(attrs={'class': 'input-medium'}),
        }

class ItemInline(admin.StackedInline):
    form = FormItemInline
    model = OrderItem
    extra = 1
    verbose_name_plural = 'Detail Order Item'
    can_delete = True
    fieldsets = [
        (None, {
            'fields': ['color', 'category', ('weight', 'capacity'), ('height', 'diameter'), 'image', 'label', 'quantity'
            , 'price']
        })
    ]

    def get_formset(self, request, obj=None):
        formset = super(ItemInline, self).get_formset(request, obj)

        if obj is not None and obj.status in (SO_FINISH_STATUS):
            formset.max_num = 0
            formset.can_delete = False
        if obj is not None:
            formset.extra = 0
        return formset

    def get_readonly_fields(self, request, obj=None):
        readonly = super(ItemInline, self).get_readonly_fields(request, obj)

        if getattr(obj, 'status', None) in (SO_FINISH_STATUS):
            readonly = ('color', 'category', 'capacity', 'height', 'weight', 'diameter', 'image', 'label', 'quantity', 'price')
        return readonly

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            request = kwargs.pop("request", None)
            kwargs['widget'] = ProductImage
            return db_field.formfield(**kwargs)
        elif db_field.name == 'label':
            request = kwargs.pop("request", None)
            kwargs['widget'] = ProductImage
            return db_field.formfield(**kwargs)
        return super(ItemInline,self).formfield_for_dbfield(db_field, **kwargs)

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

class ProductImage(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img width="100px" height="110px" src="%s" alt="%s" /></a> %s ' % \
                (image_url, image_url, file_name, _(' ')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class CorpChoices(AutoModelSelect2Field):
    queryset = Company.objects.all()
    search_fields = ['corporate__icontains']


class FormRequestOrder(forms.ModelForm):
    corp_verbose_name = 'Nama Perusahaan'
    customer = CorpChoices(label=corp_verbose_name.capitalize(),
                           widget=AutoHeavySelect2Widget(select2_options=
                                                              {'width': '220px', 'placeholder': 'Cari %s ...'
                                                                                                % corp_verbose_name}))
    class Meta:
        model = RequestOrder
        widgets = {
            'quotation': AutosizedTextarea(attrs={'rows': '5'}),
            'date': SuitDateWidget
        }


class RequestOrderAdmin(admin.ModelAdmin):
    form = FormRequestOrder
    list_display = ['number', 'customer', 'status', 'date', 'payment_term', 'tax',]
    inlines = [ItemInline]
    search_fields = ['number', 'customer__corporate', 'customer__name']
    list_filter = ['status', 'payment_term', 'shipping_methods']
    date_hierarchy = 'date'
    actions = ["generate_order"]
    list_per_page = 20

    fieldsets = [
        (None, {
            'fields': ['po_reference', 'date', 'customer', 'quotation']
        }),
    ]

    def suit_cell_attributes(self, obj, column):
        if column == 'date':
            return {'class': 'text-center'}
        elif column == 'payment_term':
            return {'class': 'text-center'}
        elif column == 'status':
            return {'class': 'text-center'}
        elif column == 'tax':
            return {'class': 'text-center'}
        elif column == 'display_price':
            return {'class': 'text-center'}

    def generate_order(self, request, queryset):
        rows_updated = queryset.update(status=2)

        if rows_updated == 1:
            message_bit = "1 Order Permintaan"
        else:
            message_bit = "%s Order Permintaan" % rows_updated
        self.message_user(request, "%s berhasil disetujui menjadi Order Penawaran" % message_bit)
    generate_order.short_description = "Buat Order Penawaran"

    def queryset(self, request):
        if request.user.is_staff:
            return SalesOrder.objects.filter(Q(status=1) | Q(status=4))
        return SalesOrder.objects.filter(Q(status=1)  | Q(status=4))

admin.site.register(RequestOrder, RequestOrderAdmin)


class FormQuoteOrder(forms.ModelForm):
    corp_verbose_name = 'Nama Perusahaan'
    customer = CorpChoices(label=corp_verbose_name.capitalize(),
                           widget=AutoHeavySelect2Widget(select2_options=
                                                              {'width': '220px', 'placeholder': 'Cari %s ...'
                                                                                                % corp_verbose_name}))

    class Meta:
        model = QuoteOrder
        widgets = {
            'quotation': AutosizedTextarea(attrs={'rows': '3'}),
            'term_service': AutosizedTextarea(attrs={'rows': '3'}),
            'shipping_address': AutosizedTextarea(attrs={'rows': '3'}),
            'date': SuitDateWidget
        }
    """
    def __init__(self, request, *args, **kwargs):
        super(FormQuoteOrder, self).__init__(*args, **kwargs)
        if None:
            self.initial.update({'sales_person': request.user}),
        else:
            pass
    """
class QuoteOrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'customer', 'sales_person','status', 'date', 'payment_term', 'tax', 'display_price']
    inlines = [ItemInline]
    search_fields = ['number', 'customer__corporate', 'customer__name']
    list_filter = ['status', 'payment_term', 'shipping_methods']
    date_hierarchy = 'date'
    actions = ["edit_order", 'generate_order', 'create_delivery_order']
    form = FormQuoteOrder
    suit_form_tabs = ( ('keterangan', 'Data Kontrak'), ('permintaan', 'Data Permintaan'),)
    readonly_fields = ('display_price',)
    exclude = ['total']
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-keterangan',),
            'fields': ('status', 'payment_type', 'payment_term', 'currency', 'tax', 'shipping_methods', 'sales_type',
                       'shipping_address','term_service', 'display_price')
        }),
         (None, {
            'classes': ('suit-tab suit-tab-permintaan',),
            'fields': ['po_reference', 'customer', 'date', 'quotation']
        })
    ]

    def suit_cell_attributes(self, obj, column):
        if column == 'date':
            return {'class': 'text-center'}
        elif column == 'payment_term':
            return {'class': 'text-center'}
        elif column == 'status':
            return {'class': 'text-center'}
        elif column == 'tax':
            return {'class': 'text-center'}
        elif column == 'display_price':
            return {'class': 'text-center'}

    def queryset(self, request):
        if request.user.is_staff:
            return SalesOrder.objects.filter(status=2)
        return SalesOrder.objects.filter(status=2)

    def edit_order(self, request, queryset):
        rows_updated = queryset.update(status=1)

        if rows_updated == 1:
            message_bit = "1 Order Penawaran"
        else:
            message_bit = "%s Order Penawaran" % rows_updated
        self.message_user(request, "%s berhasil diganti menjadi Order Permintaan" % message_bit)
    edit_order.short_description = "Edit Order Penawaran"

    def generate_order(self, request, queryset):
        rows_updated = queryset.update(status=3)

        if rows_updated == 1:
            message_bit = "1 Order Penawaran"
        else:
            message_bit = "%s Order Penawaran" % rows_updated
        self.message_user(request, "%s berhasil disetujui menjadi Order Penjualan" % message_bit)
    generate_order.short_description = "Buat Order Penjualan"

    def get_readonly_fields(self, request, obj=None):
        readonly = super(QuoteOrderAdmin, self).get_readonly_fields(request, obj)

        if getattr(obj, 'status', None) in SO_FINISH_STATUS:
            readonly = ('number', 'customer', 'po_reference', 'status', 'date', 'payment_term', 'payment_type',
                        'currency', 'shipping_methods', 'tax', 'total', 'quotation', 'term_service', 'sales_person',
                        'sales_type', 'shipping_address')
        return readonly
admin.site.register(QuoteOrder, QuoteOrderAdmin)


class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'customer', 'status', 'date', 'payment_term', 'tax', 'display_price', 'print_pdf']
    inlines = [ItemInline]
    search_fields = ['number', 'customer__corporate', 'customer__name']
    list_filter = ['status', 'payment_term', 'shipping_methods']
    date_hierarchy = 'date'
    actions = ["edit_order", 'create_invoice', 'create_delivery_order']
    form = FormQuoteOrder
    suit_form_tabs = (('permintaan', 'Data Permintaan'), ('keterangan', 'Data Kontrak'))
    exclude = ['total']
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-permintaan',),
            'fields': ['customer', 'date', 'quotation', 'status']
        }),

        (None, {
            'classes': ('suit-tab suit-tab-keterangan',),
            'fields': ('payment_type', 'payment_term', 'currency', 'tax', 'shipping_methods', 'sales_type',
                       'shipping_address','term_service',)
        })
    ]

    def suit_cell_attributes(self, obj, column):
        if column == 'date':
            return {'class': 'text-center'}
        elif column == 'payment_term':
            return {'class': 'text-center'}
        elif column == 'status':
            return {'class': 'text-center'}
        elif column == 'tax':
            return {'class': 'text-center'}
        elif column == 'display_price':
            return {'class': 'text-center'}
        elif column == 'print_pdf':
            return {'class': 'text-center'}

    def queryset(self, request):
        if request.user.is_staff:
            return SalesOrder.objects.filter(status=3)
        return SalesOrder.objects.filter(status=3)

    def edit_order(self, request, queryset):
        rows_updated = queryset.update(status=2)

        if rows_updated == 1:
            message_bit = "1 Order Penjualan"
        else:
            message_bit = "%s Order Penjualan" % rows_updated
        self.message_user(request, "%s berhasil diganti menjadi Order Penawaran" % message_bit)
    edit_order.short_description = "Edit Order Penjualan"

    def get_readonly_fields(self, request, obj=None):
        readonly = super(SalesOrderAdmin, self).get_readonly_fields(request, obj)

        if getattr(obj, 'status', None) in SO_FINISH_STATUS:
            readonly = ('number', 'customer', 'po_reference', 'status', 'date', 'payment_term', 'payment_type',
                        'currency', 'shipping_methods', 'tax', 'total', 'quotation', 'term_service', 'sales_person',
                        'sales_type', 'shipping_address')
        return readonly

admin.site.register(SalesOrder, SalesOrderAdmin)


from Apps.Distribution.master_sales.models import StaffPerson
from django.contrib.auth.admin import CustomStaffAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee', 'department', 'section']
    raw_id_fields = ['user']
    list_filter = ['user', 'employee']
    search_fields = ['user', 'employee']

admin.site.register(StaffPerson, StaffAdmin)


class InlineStaff(admin.StackedInline):
    model = StaffPerson
    extra = 1
    verbose_name_plural = 'Data Staff'
    verbose_name = 'Staff '
    max_num = 1


class CustomStaffForm(UserChangeForm):
    class Meta:
        widgets = {
            'last_login': SuitSplitDateTimeWidget,
            'date_joined': SuitSplitDateTimeWidget,
        }


class UserStaff(User):
    class Meta:
        proxy = True
        verbose_name_plural = 'Akun Staff'
        verbose_name = 'Akun Staff'
        ordering = ["id"]

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        self.is_staff = True
        super(UserStaff, self).save()


class UserStaffAdmin(CustomStaffAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', )
    list_filter = ('is_active', 'is_staff', 'date_joined', 'last_login')
    list_editable = ('is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    form = CustomStaffForm

    def suit_cell_attributes(self, obj, column):
        if column == 'is_active':
            return {'class': 'text-center'}
        elif column == 'is_staff':
            return {'class': 'text-center'}

    def queryset(self, request):
        if request.user.is_staff:
            return UserStaff.objects.filter(Q(is_staff=True))

admin.site.register(UserStaff, UserStaffAdmin)
