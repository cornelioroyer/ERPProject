''' @author: Fery Febriyan Syah '''


from django.contrib import admin
from django import forms
from Apps.Hrm.Data_Personel_Management.models import *
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitSplitDateTimeWidget, AutosizedTextarea, EnclosedInput


class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        widgets = {
            #'address': AutosizedTextarea(attrs={'rows': '3'}),
            'weight': EnclosedInput(prepend='kg', append='kg', attrs={'class': 'input-medium'}),
            'high': EnclosedInput(prepend='cm', append='cm', attrs={'class': 'input-medium'}),
        }
        
class GroupDecreeAdminForm(forms.ModelForm):
    class Meta:
        model = Group_Increase_Decree
        widgets = {
            #'address': AutosizedTextarea(attrs={'rows': '3'}),
            'working_life': EnclosedInput(append='Tahun', attrs={'class': 'input-medium'}),
        }

class PeriodicDecreeAdminForm(forms.ModelForm):
    class Meta:
        model = Periodic_Increase_Decree
        widgets = {
            #'address': AutosizedTextarea(attrs={'rows': '3'}),
            'working_life': EnclosedInput(append='Tahun', attrs={'class': 'input-medium'}),
        }


class PositionInline(admin.StackedInline):
    model = Position
    extra = 0
    verbose_name_plural = "JABATAN"
    verbose_name = "Catatan Jabatan Pegawai"
    field = ['master_position','date_decree','number_decree','level_position','group','date_promotion','unit_work',]  
    max_num = 5
    

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0
    verbose_name_plural = "PENDIDIKAN"
    verbose_name = "Catatan Pendidikan"
    field = ['education_name','institution','major','predicate',]  
    max_num = 10
    
    
class SeminarInline(admin.StackedInline):
    model = Seminar
    extra = 0
    verbose_name_plural = "SEMINAR"
    verbose_name = "Catatan Seminar"
    field = ['seminar_name','seminar_genre','basic_knowledge','city','organized',]  
    max_num = 10
    
class TaskInline(admin.StackedInline):
    model = Task
    extra = 0
    verbose_name_plural = "Tugas"
    verbose_name = "Catatan Tugas Dinas"
    field = ['task','city','Duration','in_order_to',]  
    max_num = 10  


class EmployeeAdmin(admin.ModelAdmin):    
    list_display =('employee','birthday','religion','gender','status_employee','nip','department','group','display_image')
    list_filter = ('employee','nip','group')
    search_fields = ['employee']
    inlines = [PositionInline,EducationInline,SeminarInline,TaskInline]
    form = EmployeeAdminForm
            
    def get_readonly_fields(self, request, obj=None):
        data = Group.objects.get(user=request.user)
        readonly_fields = ()
        if data.name == 'Admin':
                readonly_fields = ()
            
        elif data.name == 'Direktur':
                readonly_fields += ('employee','birthday','religion','gender','status_employee','nip','department','group','display_image',)
                    
        if request.user.is_superuser:
            readonly_fields = ()
        return readonly_fields

    
admin.site.register (Employee, EmployeeAdmin)  

class PositionAdmin(admin.ModelAdmin):
    list_display = ('employee','master_position','department','level_position','date_decree','number_decree','group','date_promotion','unit_work')  
    list_filter = ('master_position', 'level_position', 'group','department')
    search_fields = ['employee', 'master_positon']

admin.site.register (Position, PositionAdmin)
    
    
class GroupIncreaseDecreeInline(admin.StackedInline):
    model = Group_Increase_Decree
    extra = 0
    verbose_name_plural = "SK Kenanikan Golongan"
    verbose_name = "Detail SK Kenaikan Golongan"
    field = ['group','number_group_increase_decree','number_periodic_increase_decree','working_life','promotion_date','expiration_date','delayed','accelerated',]  
    max_num = 10
    form = GroupDecreeAdminForm  
    
class Periodic_Increase_DecreeAdmin (admin.ModelAdmin):
    list_display =('employee','group','number_periodic_increase_decree','working_life','promotion_date','expiration_date','delayed')    
    list_filter = ('group','number_periodic_increase_decree')
    search_fields = ['employee','group']
    inlines = [GroupIncreaseDecreeInline]
    form = PeriodicDecreeAdminForm
    
admin.site.register (Periodic_Increase_Decree, Periodic_Increase_DecreeAdmin)
    
class Group_Increase_DecreeAdmin (admin.ModelAdmin):
    list_display =('group','number_group_increase_decree','number_periodic_increase_decree','working_life','promotion_date','expiration_date','delayed','accelerated')    
    list_filter = ('group','number_group_increase_decree')
    search_fields = ['group']
    form = GroupDecreeAdminForm
    
admin.site.register (Group_Increase_Decree, Group_Increase_DecreeAdmin)
    
class EducationAdmin (admin.ModelAdmin):
    list_display =('employee','education_name','institution','major','predicate')    
    list_filter = ('education_name',)
    search_fields = ['employee']
 
admin.site.register (Education, EducationAdmin)   


class HobbyInline(admin.TabularInline):
    model = Hobby
    extra = 0
    verbose_name_plural = "HOBI"
    verbose_name = "Catatan Hobi"
    field = ['hobby_name','city','hobby_genre','achievement','apreciation_name']  
    max_num = 10  

class AppreciationAdmin (admin.ModelAdmin):
    list_display = ('employee','appreciation_name','year','in_order_to','giver')    
    list_filter = ('appreciation_name','year')
    search_fields = ['employee']
    inlines = [HobbyInline]
    
admin.site.register (Appreciation, AppreciationAdmin) 
   
   
class HobbyAdmin (admin.ModelAdmin):
    list_display = ('employee','hobby_name','hobby_genre','appreciation_name','achievement')    
    list_filter = ('hobby_genre',)
    search_fields = ['employee','hobby_name']
    
admin.site.register (Hobby, HobbyAdmin)
 
 
class SeminarAdmin (admin.ModelAdmin):
    list_display = ('employee','seminar_name','seminar_genre','basic_knowledge','city','organized',)    
    list_filter = ['seminar_genre',]
    search_fields = ['employee']
    
admin.site.register (Seminar, SeminarAdmin)
    
    
class TaskAdmin (admin.ModelAdmin):
    list_display = ('employee','task','city','in_order_to')    
    list_filter = ['task']
    search_fields = ['employee']
    
admin.site.register (Task, TaskAdmin)
    
    
class LeaveAdmin (admin.ModelAdmin):
    list_display = ('employee','leave','from_date','end_date','status')    
    list_filter = ('leave',)
    search_fields = ['employee']
    
admin.site.register (Leave, LeaveAdmin)
        
        
class SanctionAdmin (admin.ModelAdmin):
    list_display = ('employee','sanction','from_date','end_date',)    
    list_filter = ('sanction',)
    search_fields = ['employee']

admin.site.register (Sanction, SanctionAdmin)


class TerminationAdmin (admin.ModelAdmin):
    list_display = ('employee','termination','status',)    
    list_filter = ('termination',)
    search_fields = ['employee']
    
admin.site.register (Termination, TerminationAdmin)

class MutationAdmin (admin.ModelAdmin):
    list_display = ('employee','group','department_now','from_date',)
    list_filter = ('group',)
    search_fields = ['emlpoyee']

admin.site.register (Mutation, MutationAdmin)
