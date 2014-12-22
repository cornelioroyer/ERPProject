''' @author: Fery Febriyan Syah '''


from django.contrib import admin
from Apps.Hrm.Salary.models import *

class Salary_EmployeeInline(admin.StackedInline):
    model = Salary_Employee
    extra = 0
    verbose_name_plural = "GAJI"
    verbose_name = "Detail Gaji Pegawai"
    field = ['header','date_now','basic_salary','operasional_support','transport_Support','shift_operational_support','shift_operational_supporting','position_support','life_cost_support',]  
    max_num = 5

class Cut_Of_SalaryInline(admin.StackedInline):
    model = Cut_Of_Salary
    extra = 0
    verbose_name_plural = "Potongan"
    verbose_name = "Detail Potongan Pegawai"
    field = ['bulan','display_kpr', 'display_tht','display_bpjs','display_coorperation_contribution','display_sp_contribution','display_coorperation_discount','display_ykkpi',]  
    max_num = 5

class Header_SalaryAdmin (admin.ModelAdmin):
    list_display = ('employee','group','section','period','print_pdf','lock',)
    search_field = ['employee']
    inlines = [Salary_EmployeeInline,Cut_Of_SalaryInline]
    
admin.site.register(Header_Salary, Header_SalaryAdmin)

class Salary_EmployeeAdmin (admin.ModelAdmin):
    list_display = ('header','date_now','basic_salary','operasional_support','transport_Support','shift_operational_support','shift_operational_supporting','position_support','life_cost_support',)
    
admin.site.register(Salary_Employee, Salary_EmployeeAdmin)


class Cut_Of_SalaryAdmin (admin.ModelAdmin):
    list_display = ('bulan','display_kpr', 'display_tht','display_bpjs','display_coorperation_contribution','display_sp_contribution','display_coorperation_discount','display_ykkpi',)
    
admin.site.register(Cut_Of_Salary, Cut_Of_SalaryAdmin)

class Total_SalaryAdmin (admin.ModelAdmin):
    list_display = ('header','month','employee','total')
    
admin.site.register(Total_Salary, Total_SalaryAdmin)    

class Tr_PayrollAdmin(admin.ModelAdmin):   
    list_display = ('Payroll_No','Paid_Amount','Payment_Method','Date','Memo',)
    list_filter = ('Payroll_No',)
    ordering = ('-id', )
    exclude= ('Period','Payment_Status',)
    search_fields = ['']

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Tr_Payroll, Tr_PayrollAdmin)
