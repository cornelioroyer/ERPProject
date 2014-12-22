from django.contrib import admin
from Apps.Distribution.order.admin import FormItemInline
from Apps.Distribution.sales_return.models import DetailReturn, Sales_Return
from Apps.Distribution.order.models import SalesOrder
from django import forms
from suit.widgets import AutosizedTextarea, SuitDateWidget
from Apps.Distribution.customer.models import Company
from django_select2 import AutoModelSelect2Field, AutoHeavySelect2Widget


class CorpChoices(AutoModelSelect2Field):
    queryset = Company.objects.all()
    search_fields = ['corporate__icontains']

class SOChoices(AutoModelSelect2Field):
    queryset = SalesOrder.objects.filter(status=3)
    search_fields = ['number__icontains']


class FormReturnOrder(forms.ModelForm):
    corp_verbose_name = 'Nama Perusahaan'
    customer = CorpChoices(label=corp_verbose_name.capitalize(),
                           widget=AutoHeavySelect2Widget(select2_options=
                                                              {'width': '220px', 'placeholder': 'Cari %s ...'
                                                                                                % corp_verbose_name}))
    so_verbose_name = 'Nomer SO'
    so_reff = SOChoices(label=so_verbose_name.capitalize(),
                           widget=AutoHeavySelect2Widget(select2_options=
                                                              {'width': '220px', 'placeholder': 'Cari %s ...'
                                                                                                % so_verbose_name}))
    class Meta:
        model = Sales_Return
        widgets = {
            'date': SuitDateWidget
        }
class ItemReturn(admin.StackedInline):
    form = FormItemInline
    model = DetailReturn
    extra = 1
    verbose_name_plural = 'Detail Return Item'
    can_delete = True

class ReturnAdmin(admin.ModelAdmin):
    form = FormReturnOrder
    list_display = ['so_reff', 'number', 'customer', 'date', 'status', 'type_return', 'handling']
    list_filter = ['status', 'type_return', 'handling']
    search_fields = ['so_reff', 'number', 'customer',]
    date_hierarchy = 'date'
    inlines = [ItemReturn]
admin.site.register(Sales_Return, ReturnAdmin)