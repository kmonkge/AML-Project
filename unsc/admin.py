from django.contrib import admin
from django.contrib.auth.models import User
from .models import UNSCType, UNSCList, Regulator, CompanyType, Company, ComplianceOfficer, Compliance, PositiveCompliance, UNSCMemoTableFunction, User

# Register your models here.
admin.site.register(UNSCType)
admin.site.register(Regulator)
admin.site.register(CompanyType)


@admin.register(UNSCList)
class UNSCListAdmin(admin.ModelAdmin):
    list_display = ['memo_name', 'memo_type', 'slug','created_by']
    prepopulated_fields = {'slug': ('memo_name',)}

@admin.register(UNSCMemoTableFunction)
class UNSCMemoTableFunctionAdmin(admin.ModelAdmin):
    list_display = ['memo', 'slug', 'memo_type', 'company','is_exist']
    


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name','company_type','slug']
    prepopulated_fields = {'slug': ('company_name',)}


@admin.register(ComplianceOfficer)
class ComplianceOfficerAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'is_active']
    
    

@admin.register(Compliance)
class ComplianceAdmin(admin.ModelAdmin):
    list_display = ['memo_name','company','officer', 'match', 'information','is_complete']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email', 'is_regulator', 'is_officer']


@admin.register(PositiveCompliance)
class PositiveComplianceAdmin(admin.ModelAdmin):
    list_display = ['compliance','company','officer', 'unsc_reference_number', 'list_type', 'action', 'information','is_complete']
