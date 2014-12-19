__author__ = 'FARID ILHAM Al-Q'

from django.contrib import admin
from Apps.Distribution.customer.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.admin import UserAdmin, CustomUserAdmin
from suit.widgets import SuitSplitDateTimeWidget, AutosizedTextarea
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class SuitUserChangeForm(UserChangeForm):
    class Meta:
        widgets = {
            'last_login': SuitSplitDateTimeWidget,
            'date_joined': SuitSplitDateTimeWidget,
        }


class SuitAdminUser(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_editable = ('is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    form = SuitUserChangeForm

    def suit_cell_attributes(self, obj, column):
        if column == 'is_staff':
            return {'class': 'text-center'}
        elif column == 'is_active':
            return {'class': 'text-center'}

admin.site.unregister(User)
admin.site.register(User, SuitAdminUser)


class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = Company
        widgets = {
            'address': AutosizedTextarea(attrs={'rows': '3'}),
        }


from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
class CustomerImage(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img width="150px" height="150px" src="%s" alt="%s" /></a> %s ' % \
                (image_url, image_url, file_name, _(' ')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-data',),
            'fields': ['user', 'name', 'position', 'type', 'corporate', 'phone', 'business', 'industry', 'npwp', 'logo']}),
        (None, {
            'classes': ('suit-tab suit-tab-info',),
            'fields': ('region','email', 'city', 'province', 'zip_code', 'country', 'currency', 'address', 'fax', 'website'),
        }),
        (None, {
            'classes': ('suit-tab suit-tab-bank',),
            'fields': ('bank_name', 'bank_branch', 'bank_account_name', 'rek',)
        })

    )

    suit_form_tabs = (('data', 'Data Perusahaan'), ('info', 'Info Perusahaan'), ('bank', 'Info Bank'))
    form = CustomerAdminForm
    list_display = ['name', 'type', 'corporate', 'email', 'business', 'industry', 'country', 'display_image' ]
    search_fields = ['name', 'type', 'position', 'corporate', 'email']
    raw_id_fields = ('user',)
    list_filter = ['type', 'business', 'industry']
    list_per_page = 5

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'logo':
            request = kwargs.pop("request", None)
            kwargs['widget'] = CustomerImage
            return db_field.formfield(**kwargs)
        return super(CustomerAdmin,self).formfield_for_dbfield(db_field, **kwargs)

    def suit_cell_attributes(self, obj, column):
        if column == 'display_image':
            return {'class': 'text-center'}

admin.site.register(Company, CustomerAdmin)


class CompanyInlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            'address': AutosizedTextarea(attrs={'rows': '3'}),
        }


class CompanyInline(admin.StackedInline):
    model = Company
    extra = 0
    form = CompanyInlineForm
    verbose_name_plural = _('Data Perusahaan')
    verbose_name = _('Perusahaan ')
    max_num = 1

    fieldsets = (
        (None, {
            'fields': ['user', 'name', 'position', 'type', 'corporate', 'phone', 'business', 'industry', 'npwp', 'logo']}),
        ('Info Perusahaan', {
            'classes': ('collapse',),
            'fields': ('email', 'city', 'province', 'zip_code', 'country', 'address', 'fax', 'website'),
        }),
        ('Rekening Bank :', {
            'classes': ('collapse',),
            'fields': ('bank_name', 'bank_branch', 'bank_account_name', 'rek',)
        })
    )


class CustomerUserAdmin(CustomUserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active',)
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    form = SuitUserChangeForm
    list_per_page = 15
    inlines = [CompanyInline]

    def suit_cell_attributes(self, obj, column):
        if column == 'is_active':
            return {'class': 'text-center'}

    def queryset(self, request):
        if request.user.is_staff:
            return UserCompany.objects.filter(Q(is_staff=False))
"""
    def has_add_permission(self, request):
        from django.contrib.auth.models import Group
        data = Group.objects.get(user=request.user)
        if data.name == "staf_penjualan":
            return True
        else: return False

    def has_change_permission(self, request, obj=None):
        from django.contrib.auth.models import Group
        data = Group.objects.get(user=request.user)
        if data.name == "staf_penjualan":
            return True
        else: return False
    def has_delete_permission(self, request, obj=None):
        from django.contrib.auth.models import Group
        data = Group.objects.get(user=request.user)
        if data.name == "staf_penjualan":
            return True
        else: return False
"""
admin.site.register(UserCompany, CustomerUserAdmin)
