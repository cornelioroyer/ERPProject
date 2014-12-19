__author__ = 'FARID ILHAM Al-Q'
from django.contrib import admin
from Apps.Distribution.CRM.models import *


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'country', 'company', 'referral', 'pub_date']
    fieldsets = (
        (None, {
            'fields': ('name', 'company', 'email', 'phone', 'country', 'referral', 'comment')}),
    )
    search_fields = ['name', 'email', 'phone', 'country', 'company', 'referral']
    list_filter = ['email', 'phone', 'pub_date']
    list_per_page = 20
admin.site.register(Contacts, ContactAdmin)


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'pub_date', 'update']
    list_filter = ['pub_date', 'update']
    search_fields = ['title']
    list_per_page = 20
admin.site.register(News, NewsAdmin)


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['customer', 'status', 'about', 'created']
    list_filter = ['status']
    search_fields = ['customer', 'description']
    list_per_page = 20
admin.site.register(Complaint, ComplaintAdmin)
