"""Develop By - Achmad Afiffudin N"""

from django.contrib import admin
from Apps.Accounting.GeneralLedger.models import *
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import HttpResponse
from django import forms
from django.forms import TextInput, Select
from django.contrib.admin.views.main import ChangeList
from django.db.models import Avg, Sum
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.conf.urls import patterns, include, url
from admin_decorators import allow_tags
from suit.widgets import *
from django_select2 import *
from django.contrib.auth.models import *
from mptt.admin import MPTTModelAdmin
from suit.admin import SortableModelAdmin

class FormAccount(forms.ModelForm):
    class Meta:
        widgets = {
            'Account_Code': TextInput(attrs={'class': 'input-medium'}),
            'Account_Name': TextInput(attrs={'class': 'input-medium'}),
            'Account_Type': LinkedSelect(attrs={'class': 'input-medium'}),
            'parent': LinkedSelect(attrs={'class': 'input-medium'})
        }

class Ms_AccountAdmin(MPTTModelAdmin, SortableModelAdmin):
    form = FormAccount
    mptt_level_indent = 15
    list_display = ('Account_Code','Account_Name','Account_Type','Status',)
    list_filter = ('Account_Type',)
    search_fields = ('Account_Name',)
    list_per_page = 20
    list_display_links = ('Account_Name',)
    sortable = 'order'

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Account_Code','Account_Name','Account_Type','parent','Status')
        return readonly_fields

admin.site.register(Ms_Account, Ms_AccountAdmin)

class FormFiscalYear(forms.ModelForm):
    class Meta:
        widgets = {
            'Fiscal_Year': TextInput(attrs={'class': 'input-medium'}),
            'Code': TextInput(attrs={'class': 'input-mini'}),
            'Start_Fiscal': SuitDateWidget,
            'End_Fiscal': SuitDateWidget
        }

class Ms_Fiscal_YearsAdmin(admin.ModelAdmin):
    list_display = ('Fiscal_Year','Code','Start_Fiscal','End_Fiscal',)
    search_fields = ('Code',)
    ordering = ('-Start_Fiscal','-End_Fiscal',)
    exclude = ['Status',]
    list_per_page = 15
    form = FormFiscalYear
    fieldsets = [(None, {
        'fields': ['Code','Fiscal_Year','Start_Fiscal','End_Fiscal',]
    })]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Code','Fiscal_Year','Start_Fiscal','End_Fiscal',)
        return readonly_fields

    def suit_row_attributes(self, obj, request):
		css_class = {
			1: 'success',2: 'error',}.get(obj.status())
		if css_class:
			return {'class': css_class, 'data': obj.status()}

admin.site.register(Ms_Fiscal_Years, Ms_Fiscal_YearsAdmin)

class FisChoices(AutoModelSelect2Field):
    queryset = Ms_Fiscal_Years.objects.all()
    search_fields = ['Fiscal_Year']

class FormPeriod(forms.ModelForm):
    class Meta:
        widgets = {
            'Period_Name': TextInput(attrs={'class': 'input-medium'}),
            'Code': TextInput(attrs={'class': 'input-mini'}),
            'Fiscal_Year': LinkedSelect(attrs={'class': 'input-small'}),
            'Start_Period': SuitDateWidget,
            'End_Period': SuitDateWidget
        }

class Ms_PeriodAdmin(admin.ModelAdmin):
    list_display = ('Period_Name','Code','Fiscal_Year','Start_Period','End_Period',)
    list_filter = ('Fiscal_Year__Fiscal_Year',)
    search_fields = ('Period_Name',)
    ordering = ['-Start_Period','-End_Period',]
    form = FormPeriod
    actions = ['status',]
    exclude = ('Status',)
    list_per_page = 15

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Period_Name','Code','Fiscal_Year','Start_Period','End_Period',)
        return readonly_fields

    def suit_row_attributes(self, obj, request):
		css_class = {
			1: 'success',2: 'error',}.get(obj.status())
		if css_class:
			return {'class': css_class, 'data': obj.status()}

    def status(self, request, queryset):
        rows_updated = queryset.update(Status=1)
        if rows_updated == 1:
            message_bit = "1 Periode"
        else:
            message_bit = "%s Periode" % rows_updated
        self.message_user(request, "%s Terbuka" % message_bit)
    status.short_description = "Buka Periode"

admin.site.register(Ms_Period, Ms_PeriodAdmin)

class FormJournal(forms.ModelForm):
    class Meta:
        widgets = {
            'Journal_Name': TextInput(attrs={'class': 'input-medium'}),
            'Code': TextInput(attrs={'class': 'input-medium'}),
            'Type': LinkedSelect(attrs={'class': 'input-medium'}),
        }

class Ms_JournalAdmin(admin.ModelAdmin):
    form = FormJournal
    list_display = ('Journal_Name','Code','Type',)
    list_filter = ('Type',)
    search_fields = ['Journal_Name','Code','Type',]
    ordering = ('-Code',)

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Journal_Name','Code','Type',)
        return readonly_fields

admin.site.register(Ms_Journal, Ms_JournalAdmin)

class Detail_Journal_EntryInline(admin.TabularInline):
    model = Detail_Journal_Entry
    can_delete = False
    editable_fields = []
    verbose_name_plural = 'Journal Item'
    list_per_page  = 10

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields = ('Date','Reference','Account','Journal_Entry','Debit','Credit',)
        return readonly_fields
    
    def has_add_permission(self, request):
        return False

class FormEntry(forms.ModelForm):
    class Meta:
        widgets = {
            'Journal_Entry_No': TextInput(attrs={'class': 'input-large'}),
            'Reference': TextInput(attrs={'class': 'input-large'}),
            'Journal': LinkedSelect(attrs={'class': 'input-medium'}),
            'Journal_Period': LinkedSelect(attrs={'class': 'input-medium'}),
            'Status': LinkedSelect(attrs={'class': 'input-medium'}),
            'Date': SuitDateWidget
        }

class Tr_Journal_EntryAdmin(admin.ModelAdmin):
    list_display = ('Journal_Entry_No','Journal','Journal_Period','Reference','Date','Status',)
    list_filter = ('Journal','Journal_Period','Journal_Period__Fiscal_Year__Fiscal_Year','Status')
    search_fields = ('Journal_Entry_No',)
    ordering = ('-Journal_Entry_No',)
    actions = ['edit_status']
    inlines = [Detail_Journal_EntryInline,]
    date_hierarchy = 'Date'
    list_per_page = 10
    form = FormEntry

    def get_readonly_fields(self, request, obj=None):
        get = 1
        readonly_fields = ()
        try:
			per = getattr(obj, 'Journal_Period', None)
			get = per.Fiscal_Year.status()
        except:
            pass
        if request.user.is_superuser:
            readonly_fields = ('memo',)
        else:
            if getattr(obj, 'Status', None) == 2 or get == 2:
                readonly_fields = ('Journal_Entry_No','Journal','Journal_Period','Reference','Date','Status','memo')
        return readonly_fields 
        
    def get_form(self, request, obj=None, **kwargs):
        form = super(Tr_Journal_EntryAdmin, self).get_form(request, obj, **kwargs)
        self.exclude = ()
        get = 1
        try:
			per = getattr(obj, 'Journal_Period', None)
			get = per.Fiscal_Year.status()
        except:
            pass
        if getattr(obj, 'Status', None) == 2 or get == 2:
            self.exclude += ('Debit','Credit','Memo')
        else:
            self.exclude += ('Debit','Credit',)
        return form           
    
    def edit_status(self, request, queryset):
        rows_updated = queryset.update(Status=2)
        if rows_updated == 1:
            message_bit = "1 Jurnal"
        else:
            message_bit = "%s Jurnal" % rows_updated
        self.message_user(request, "%s Terposting" % message_bit)
    edit_status.short_description = "Posting Ke GL"

    def status(self, request, queryset):
        rows_updated = queryset.update(Status=1)
        if rows_updated == 1:
            message_bit = "1 Jurnal"
        else:
            message_bit = "%s Jurnal" % rows_updated
        self.message_user(request, "%s Unpost" % message_bit)
    status.short_description = "Hapus Posting"

    def suit_row_attributes(self, obj, request):
		css_class = {
			2: 'success',1: 'error',}.get(obj.Status)
		if css_class:
			return {'class': css_class, 'data': obj.Status}

admin.site.register(Tr_Journal_Entry, Tr_Journal_EntryAdmin)

class Detail_Depreciation_AccountInline(admin.TabularInline):
    model = Detail_Depreciation_Account
    can_delete = False
    editable_fields = []
    verbose_name_plural = 'Akun Penyusutan'
    list_per_page  = 2
    max_num = 2

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'staf_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Depreciation','Account','Type',)
        return readonly_fields

class depresiation_record_admin(admin.ModelAdmin):
    list_display = ['period','no_reg','ref_asset','dep_no','dep_value',]
    search_fields = ['no_reg','ref_asset','dep_no']
    exclude = ['journal','period']
    readonly_fields = ['no_reg','ref_asset','dep_no','dep_value','journal','period']
    inlines = [Detail_Depreciation_AccountInline,]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('no_reg','ref_asset','dep_no','dep_value','journal','period')
        return readonly_fields

    def has_add_permission(self, request, obj=None):
        return False
            
    def get_form(self, request, obj=None, **kwargs):
        form = super(depresiation_record_admin, self).get_form(request, obj, **kwargs)
        jour=1
        try:
            jur = getattr(obj, 'journal', None)
            jour = jur.Type
        except:
            pass
        if jour==1:
            form.base_fields['journal'].queryset = form.base_fields['journal'].queryset.filter(Type=6)
        return form
        
admin.site.register(depresiation_record, depresiation_record_admin)

class Detail_Adjustment_Journal_AccountInline(admin.TabularInline):
    model = Detail_Adjustment_Journal_Account
    can_delete = False
    editable_fields = []
    verbose_name_plural = 'Akun Penyesuaian'
    list_per_page  = 2
    max_num = 2

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Adjustment','Account','Type',)
        return readonly_fields

class FormAdj(forms.ModelForm):
    class Meta:
        widgets = {
            'Adjustment_Journal_Id': TextInput(attrs={'class': 'input-large'}),
            'Journal': LinkedSelect(attrs={'class': 'input-medium'}),
            'Memo': Textarea(attrs={'rows': '4'}),
            'Adjustment_Value': NumberInput(attrs={'class': 'input-large'}),
            'Date': SuitDateWidget
        }

class Tr_Adjustment_JournalAdmin(admin.ModelAdmin):
    list_display = ('Adjustment_Journal_Id','Date','Journal','Period','Memo','Adjustment_Value',)
    list_filter = ('Journal','Period','Period__Fiscal_Year__Fiscal_Year',)
    search_fields = ['Adjustment_Journal_Id','Journal','Period','Period__Fiscal_Year__Fiscal_Year',]
    ordering = ('Adjustment_Journal_Id',)
    form = FormAdj
    inlines = [Detail_Adjustment_Journal_AccountInline,]
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Adjustment_Journal_Id','Date','Journal','Period','Memo','Adjustment_Value',)
        return readonly_fields

admin.site.register(Tr_Adjustment_Journal, Tr_Adjustment_JournalAdmin)

"""
class Detail_Journal_EntryAdmin(admin.ModelAdmin):
    list_display = ('Reference','Date','Account','Journal_Entry','Debit','Credit',)
    list_filter = ('Date','Reference','Account','Journal_Entry',)
    search_fields = ['Journal_Entry__Journal','Journal_Entry__Journal_Period','Account','Reference','Date','Status',]
    ordering = ('-Date',)

admin.site.register(Detail_Journal_Entry, Detail_Journal_EntryAdmin)

class Report(Detail_Journal_Entry):
    class Meta:
        proxy = True
        verbose_name = 'Pelaporan'
        verbose_name_plural = 'Pelaporan'

class ReportAdmin(admin.ModelAdmin):
    review_template = 'admin/accounting/gl/report.html'
    def get_url(self):
        urls = super(ReportAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^review/$', self.admin_site.admin_view(self.review)),)
        return my_urls+urls
    
    def review(self, request):
        fiscal = Ms_Fiscal_Years.objects.all()
        results = {}
        a = ''
        if request.method == 'POST' :
            if request.POST['com_fiscal'] == 'Pilih Tahun -':
                a = ''
            else :
                a = request.POST['com_fiscal']
            results = Detail_Journal_Entry.objects.filter(Journal_Entry__Journal_Period__Fiscal_Year__Fiscal_Year=a, Journal_Entry__Status=2)
        else:
            results = Detail_Journal_Entry.objects.all()

        return render_to_response(self.review_template, {
            'fiscal' : fiscal,
            'results' : results,
            'a' :a,
            'opts' : self.model._meta,
            'root_path' : self.admin_site.root_path,
            }, context_instance=RequestContext(request,{}))
admin.site.register(Report, ReportAdmin)
"""
