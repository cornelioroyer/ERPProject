''' @author: Fery Febriyan Syah '''


from django.contrib import admin
from Apps.Hrm.Recruitment.models import *
from django.utils.translation import ugettext_lazy as _



class RoleInline(admin.StackedInline):
    model = Role
    extra = 0
    verbose_name_plural = "BERKAS"
    verbose_name = "Catatan Persyaratan Khusus"
    field = ['certificate','transcript','SKCK','bill_of_health','birth_certificate','copy_ktp',]  
    max_num = 5


class Candidate_New_EmployeAdmin(admin.ModelAdmin):    
    list_display =('participant_no','applicant_name','birthday','religion','gender','national','edu_status',)
    list_filter = ('applicant_name','religion','gender',)
    search_field = ['applicant_name']
    inlines = [RoleInline]
        

class RoleAdmin(admin.ModelAdmin):
    list_display =('aplicant_name','certificate','transcript','SKCK','bill_of_health','birth_certificate','copy_ktp',)    
    search_field = ['applicant_name']
    
class TestAdmin (admin.ModelAdmin):
    list_display =('aplicant_name','date','administrasion','date','interview_1','date','psykotest','date','health','located','date','interview_2',)    
    search_field = ['applicant_name']
    
    
class ResultAdmin (admin.ModelAdmin):
    list_display =('aplicant_name','administrasion','interview_1','psykotest','health','interview_2','desicion',)    
    search_field = ['applicant_name']
    
        

admin.site.register (Candidate_New_Employe, Candidate_New_EmployeAdmin)
admin.site.register (Role, RoleAdmin)
admin.site.register (Test, TestAdmin)
admin.site.register (Result, ResultAdmin)
