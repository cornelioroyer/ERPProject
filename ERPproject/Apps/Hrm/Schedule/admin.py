''' @author: Fery Febriyan Syah '''


from django.contrib import admin
from Apps.Hrm.Schedule.models import *


class DataScheduleInline(admin.TabularInline):
    model = Data_Schedule
    extra = 1
    max_num = 1
    #readonly_fields = ('employee','department')
    

class Header_ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date_now','employee_classification','Shift','lock',)
    search_field = ['employee_classification','Shift']
    inlines = [DataScheduleInline]
    
    def suit_row_attributes(self, obj, request):
        css_class = {
            True:'success', False: 'error',}.get(obj.lock)
        if css_class:
            return {'class': css_class, 'data': obj.lock}
    
    def get_readonly_fields(self, request, object=None):
        readonly_fields = ()
        if getattr(object, 'lock', None) == True:
            readonly_fields += ('date_now',)
          
        return readonly_fields
    
admin.site.register(Header_Schedule, Header_ScheduleAdmin)


class Data_ScheduleAdmin (admin.ModelAdmin):
    list_display = ('header','employee','department')
    search_field = ['employee']
    
    def get_form(self, request, object=None, **kwargs):
        form = super(Data_ScheduleAdmin, self).get_form(request, object, **kwargs)
        xx = False
        try:
            x = getattr(object, 'header', None)
            xx = x.lock
        except: pass
        
        if xx == False:
            form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(lock=False)
        else:
            readonly_fields = ('header','employee','department')
        return form 
    
admin.site.register(Data_Schedule, Data_ScheduleAdmin)
