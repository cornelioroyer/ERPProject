from django.contrib import admin
from Apps.Distribution.order.admin import ItemInline
from Apps.Distribution.shipping.models import DeliveryOrder
from django import forms
from suit.widgets import AutosizedTextarea, SuitDateWidget
from library.const.order import DO_FINISH_STATUS
from Apps.Distribution.customer.models import Company
from Apps.Distribution.master_sales.models import StaffPerson
from django_select2 import AutoModelSelect2Field, AutoHeavySelect2Widget


class StaffChoices(AutoModelSelect2Field):
    queryset = StaffPerson.objects.all()
    search_fields = ['employee__employee_name__icontains']


class CorpChoices(AutoModelSelect2Field):
    queryset = Company.objects.all()
    search_fields = ['corporate__icontains']


class FormDeliveryOrder(forms.ModelForm):
    staff_verbose_name = 'Staff Distribusi '
    corp_verbose_name = 'Nama Perusahaan'
    staff_delivery = StaffChoices(label=staff_verbose_name.capitalize(),
                                widget=AutoHeavySelect2Widget(select2_options=
                                                              {'width': '220px', 'placeholder': 'Cari %s ...'
                                                                                                % staff_verbose_name}))
    customer = CorpChoices(label=corp_verbose_name.capitalize(),
                                widget=AutoHeavySelect2Widget(select2_options=
                                                              {'width': '220px', 'placeholder': 'Cari %s ...'
                                                                                                % corp_verbose_name}))

    class Meta:
        model = DeliveryOrder
        widgets = {
            'date': SuitDateWidget,
            'ship_date': SuitDateWidget,
            'ship_address': AutosizedTextarea(attrs={'rows': '3'}),
            'term_service': AutosizedTextarea(attrs={'rows': '3'}),
            'quotation': AutosizedTextarea(attrs={'rows': '3'}),
        }


class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'customer', 'status', 'date', 'payment_term', 'tax']
    list_filter = ['status', 'payment_term', 'shipping_methods']
    search_fields = ['number', 'so_reff', 'customer__corporate', 'customer__name']
    date_hierarchy = 'ship_date'
    inlines = [ItemInline]
    suit_form_tabs = (('pengiriman', 'Data Pengiriman'), ('keterangan', 'Data Kontrak '))
    form = FormDeliveryOrder
    actions = ['create_outpass']

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-pengiriman',),
            'fields': [ 'po_reference', 'date', 'customer', 'staff_delivery', 'status', 'ship_date', 'ship_address', 'term_service', 'quotation', 'total']
        }),

        (None, {
            'classes': ('suit-tab suit-tab-keterangan',),
            'fields': ('sales_type', 'payment_type', 'payment_term', 'currency', 'tax', 'shipping_methods')
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

    def get_readonly_fields(self, request, obj=None):
        readonly = super(DeliveryOrderAdmin, self).get_readonly_fields(request, obj)

        if getattr(obj, 'status_do', None) in DO_FINISH_STATUS :
            readonly = ('customer', 'po_reference', 'status', 'payment_term', 'payment_type',
                        'currency', 'shipping_methods', 'tax', 'total', 'quotation', 'term_service',
                        'sales_type', 'date', 'ship_date', 'shipping_address', 'staff_delivery', 'status_do')
        return readonly

admin.site.register(DeliveryOrder, DeliveryOrderAdmin)

