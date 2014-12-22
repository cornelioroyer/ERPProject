"""Develop By - Achmad Afiffudin N"""

from django.contrib import admin
from Apps.Accounting.CashBank.models import *
from django.utils.translation import ugettext as _
from suit.widgets import *
from django import forms
from django.contrib.auth.models import *

class FormCurrencyAdmin(forms.ModelForm):
    class Meta:
        model = Currency
        widgets = {
            'Code': EnclosedInput(prepend='icon-barcode', attrs={'class': 'input-small'}),
            'Rate': EnclosedInput(prepend='icon-asterisk', attrs={'class': 'input-small'}),
            'Pre_Symbol': EnclosedInput(prepend='icon-chevron-left', attrs={'class': 'input-small'}),
            'Post_Symbol': EnclosedInput(prepend='icon-chevron-right', attrs={'class': 'input-small'}),
        }

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['Name','Code','Rate','Pre_Symbol','Post_Symbol']
    list_filter = ['Code','Rate','Pre_Symbol','Post_Symbol']
    search_fields = ['Name']
    form = FormCurrencyAdmin

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_keuangan':
            readonly_fields = ()
        else:
            readonly_fields = ('Name','Code','Rate','Pre_Symbol','Post_Symbol')
        return readonly_fields

    fieldsets = [
        (None, {
            'fields': ['Name','Code','Rate','Pre_Symbol','Post_Symbol']
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
admin.site.register(Ms_Currency, CurrencyAdmin)

class Ms_TaxAdmin(admin.ModelAdmin):   
    list_display = ('Name', 'Description','Code','Percentage',)
    list_filter = ('Name',)
    ordering = ('-id', )
    search_fields = ('Name',)
    
    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_keuangan':
            readonly_fields = ()
        else:
            readonly_fields = ('Name', 'Description','Code','Percentage',)
        return readonly_fields
        
admin.site.register(Ms_Tax,Ms_TaxAdmin)

class Ms_BankAdmin(admin.ModelAdmin):
    list_display = ('Bank', 'Bank_Account','Bank_Branch','Address',)
    ordering = ('-id', )
    search_fields = ('Bank__name',)

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_keuangan':
            readonly_fields = ()
        else:
            readonly_fields = ('Bank', 'Bank_Account','Bank_Branch','Address',)
        return readonly_fields

admin.site.register(Ms_Bank, Ms_BankAdmin)

class Ms_CashAdmin(admin.ModelAdmin):
    list_display = ('Cash_No', 'Cash_Name','Description',)
    ordering = ('-id', )
    search_fields = ('Cash_Name',)

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'pengendali_keuangan':
            readonly_fields = ()
        else:
            readonly_fields = ('Cash_No', 'Cash_Name','Description',)
        return readonly_fields

admin.site.register(Ms_Cash, Ms_CashAdmin)

class FormBank(forms.ModelForm):
    class Meta:
        widgets = {
            'Reference': TextInput(attrs={'class': 'input-medium'}),
            'Date': SuitDateWidget,
            'Debit' : NumberInput(attrs={'class': 'input-medium'}),
            'Credit': NumberInput(attrs={'class': 'input-medium'})
        }

class BankInline(admin.TabularInline):
    model = Tr_Bank
    form = FormBank
    verbose_name_plural = 'Detail Transaksi'
    list_per_page  = 10
    max_num = 0
    extra = 0
    can_delete = False   
    fields = ['Reference','Date','Debit','Credit',]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields = ('Reference','Date','Debit','Credit',)
        return readonly_fields

class FormCash(forms.ModelForm):
    class Meta:
        widgets = {
            'Reference': TextInput(attrs={'class': 'input-medium'}),
            'Date': SuitDateWidget,
            'Debit' : NumberInput(attrs={'class': 'input-medium'}),
            'Credit': NumberInput(attrs={'class': 'input-medium'})
        }
    
class CashInline(admin.TabularInline):
    model = Tr_Cash
    form = FormCash
    verbose_name_plural = 'Detail Transaksi'
    list_per_page  = 10
    max_num = 0
    extra = 0
    can_delete = False    
    fields = ['Reference','Date','Debit','Credit',]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields = ('Reference','Date','Debit','Credit',)
        return readonly_fields

class BankAdmin(admin.ModelAdmin):   
    list_display = ('Bank', 'Bank_Account','Bank_Branch','Address','total',)
    ordering = ('-id', )
    search_fields = ['Bank__name',]
    inlines = [BankInline,]
    readonly_fields = ('Bank', 'Bank_Account','Bank_Branch','Address','total',)

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
        
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
        
admin.site.register(Bank, BankAdmin)

class CashAdmin(admin.ModelAdmin):   
    list_display = ('Cash_No', 'Cash_Name','Description','total',)
    ordering = ('-id', )
    search_fields = ['Cash_Name',]
    inlines = [CashInline,]
    readonly_fields = ('Cash_No', 'Cash_Name','Description','total',)

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

admin.site.register(Cash, CashAdmin)

class Detail_Adjustment_CashBankAdminInline(admin.TabularInline):
    model = Detail_Adjustment_Cash_Bank_Account
    verbose_name_plural = 'Detail Akun'
    list_per_page  = 2
    max_num = 2
    extra = 2
    can_delete = False    
    fields = ['Account','Type',]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'staf_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Account','Type',)
        return readonly_fields

class FormAdj(forms.ModelForm):
    class Meta:
        widgets = {
            'Type' : LinkedSelect(attrs={'class': 'input-large'}),
            'Date': SuitDateWidget,
            'Cash' : LinkedSelect(attrs={'class': 'input-large'}),
            'Bank' : LinkedSelect(attrs={'class': 'input-large'}),
            'Value' : NumberInput(attrs={'class': 'input-medium'}),
            'Memo': Textarea(attrs={'rows': '4'})
        }
        
class Tr_Adjustment_CashBankAdmin(admin.ModelAdmin):
    form = FormAdj
    list_display = ('Adjustmen_No', 'Type','Date','Value','Memo','Control',)
    ordering = ('Date', )
    search_fields = ['Type',]
    inlines = [Detail_Adjustment_CashBankAdminInline,]
    fieldsets = [(None, {
        'fields': ['Adjustmen_No','Type','Date','Cash','Bank','Value','Memo','Control']
    })]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser:
            readonly_fields = ()
        elif user.name == 'manager_keuangan':
            readonly_fields = ('Adjustmen_No', 'Type','Cash','Bank','Date','Journal','Period','Value','Memo',)
        elif user.name == 'pengendali_keuangan':
            readonly_fields = ('Control',)
        else:
            readonly_fields = ('Adjustmen_No', 'Type','Cash','Bank','Date','Journal','Period','Value','Memo','Control',)
        return readonly_fields

admin.site.register(Tr_Adjustment_CashBank, Tr_Adjustment_CashBankAdmin)

class Detail_Capital_BudgetAdminInline(admin.TabularInline):
    model = Detail_Capital_Budget_Account
    verbose_name_plural = 'Detail Akun'
    list_per_page  = 2
    max_num = 2
    extra = 2
    can_delete = False    
    fields = ['Account','Type',]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser or user.name == 'staf_akuntansi':
            readonly_fields = ()
        else:
            readonly_fields = ('Account','Type',)
        return readonly_fields

class FormCap(forms.ModelForm):
    class Meta:
        widgets = {
            'Date': SuitDateWidget,
            'Bank' : LinkedSelect(attrs={'class': 'input-large'}),
            'Value' : NumberInput(attrs={'class': 'input-medium'}),
            'Memo': Textarea(attrs={'rows': '4'})
        }

class Tr_Capital_BudgetAdmin(admin.ModelAdmin):
    list_display = ('Capital_Budget_No','Date','Bank','Value','Memo','Control',)
    form = FormCap
    ordering = ('Date', )
    search_fields = ['Capital_Budget_No',]
    inlines = [Detail_Capital_BudgetAdminInline,]

    def get_readonly_fields(self, request, obj=None):
        user = Group.objects.get(user=request.user)
        readonly_fields = ()
        if request.user.is_superuser:
            readonly_fields = ()
        elif user.name == 'manager_keuangan':
            readonly_fields = ('Capital_Budget_No','Date','Bank','Journal','Period','Value','Memo',)
        elif user.name == 'pengendali_keuangan':
            readonly_fields = ('Control',)
        else:
            readonly_fields = ('Capital_Budget_No','Date','Bank','Journal','Period','Value','Memo','Control',)
        return readonly_fields

admin.site.register(Tr_Capital_Budget, Tr_Capital_BudgetAdmin)
