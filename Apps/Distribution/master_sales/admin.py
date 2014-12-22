__author__ = 'FARID ILHAM Al-Q'

from django.contrib import admin
from django import forms
from suit.widgets import EnclosedInput
from Apps.Distribution.master_sales.models import *
from suit.widgets import AutosizedTextarea, SuitSplitDateTimeWidget
from django.db.models import Q
from django.utils.translation import ugettext as _


class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage']
    list_filter = ['percentage']
    search_fields = ['name']

    def suit_cell_attributes(self, obj, column):
        if column == 'percentage':
            return {'class': 'text-center'}
admin.site.register(Tax, TaxAdmin)


class FormCurrencyAdmin(forms.ModelForm):
    class Meta:
        model = Currency
        widgets = {
            'code': EnclosedInput(prepend='icon-barcode', attrs={'class': 'input-small'}),
            'rate': EnclosedInput(prepend='icon-asterisk', attrs={'class': 'input-small'}),
            'pre_symbol': EnclosedInput(prepend='icon-chevron-left', attrs={'class': 'input-small'}),
            'post_symbol': EnclosedInput(prepend='icon-chevron-right', attrs={'class': 'input-small'}),
        }


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'rate', 'pre_symbol', 'post_symbol']
    list_filter = ['code', 'rate', 'pre_symbol', 'post_symbol']
    search_fields = ['name', 'code', 'rate']
    form = FormCurrencyAdmin

    fieldsets = [
        (None, {
            'fields': ['name', 'code', 'rate', 'pre_symbol', 'post_symbol']
        })
    ]

    def suit_cell_attributes(self, obj, column):
        if column == 'pre_symbol':
            return {'class': 'text-center'}
        elif column == 'code':
            return {'class': 'text-center'}
        elif column == 'rate':
            return {'class': 'text-center'}
        elif column == 'post_symbol':
            return {'class': 'text-center'}
admin.site.register(Currency, CurrencyAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'period']
    list_filter = ['name', 'period']
    search_fields = ['name', 'description', 'period']

    def suit_cell_attributes(self, obj, column):
        if column == 'period':
            return {'class': 'text-center'}

admin.site.register(PaymentTerm, PaymentAdmin)

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe


class BankImage(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img width="200px" height="150px" src="%s" alt="%s" /></a> %s ' % \
                (image_url, image_url, file_name, _(' ')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'display_image']
    search_fields = ['name', 'description']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'logo':
            request = kwargs.pop("request", None)
            kwargs['widget'] = BankImage
            return db_field.formfield(**kwargs)
        return super(BankAdmin,self).formfield_for_dbfield(db_field, **kwargs)

    def suit_cell_attributes(self, obj, column):
        if column == 'display_image':
            return {'class': 'text-center'}
admin.site.register(Bank, BankAdmin)


class ShippingAdmin(admin.ModelAdmin):
    list_display = ['name', 'info']
    list_filter = ['name']
    search_fields = ['name', 'info']
admin.site.register(ShippingMethods, ShippingAdmin)


class FormCall(forms.ModelForm):

    class Meta:
        model = LogCall
        widgets = {'summary': AutosizedTextarea(attrs={'rows': '3'}),
                   'date': SuitSplitDateTimeWidget}


class LoggedCallAdmin(admin.ModelAdmin):
    list_display = ['customer', 'cust_name', 'no_phone', 'date', 'summary', 'status']
    search_fields = ['customer', 'summary']
    list_filter = ['date']
    form = FormCall

    fieldsets = [(None, {
        'fields': ['customer', 'duration', 'category', 'priority', 'summary', 'status', 'date',]
    })]

    def suit_cell_attributes(self, obj, column):
        if column == 'date':
            return {'class': 'text-center'}
        elif column == 'status':
            return {'class': 'text-center'}

    def queryset(self, request):
        if request.user.is_staff:
            return LogCall.objects.filter(status=1)
        return LogCall.objects.filter(status=1)

admin.site.register(LogCall, LoggedCallAdmin)


class ScheduleFormCall(forms.ModelForm):

    class Meta:
        widgets = {'summary': AutosizedTextarea(attrs={'rows': '3'}),
                   'date': SuitSplitDateTimeWidget}


class ScheduledCallAdmin(admin.ModelAdmin):
    list_display = ['customer', 'cust_name', 'no_phone', 'date', 'summary', 'status']
    search_fields = ['customer', 'summary']
    list_filter = ['date']
    form = ScheduleFormCall

    fieldsets = [(None, {
        'fields': ['customer', 'duration', 'category', 'priority', 'summary', 'status', 'date']
    })]

    def suit_cell_attributes(self, obj, column):
        if column == 'date':
            return {'class': 'text-center'}
        elif column == 'status':
            return {'class': 'text-center'}

    def queryset(self, request):
        if request.user.is_staff:
            return LogCall.objects.filter(Q(status=2) | Q(status=3))
        return LogCall.objects.filter(Q(status=2) | Q(status=3))

admin.site.register(ScheduledCall, ScheduledCallAdmin)

