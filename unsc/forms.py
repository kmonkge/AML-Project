from notification import models
from typing import ClassVar
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import Compliance, ComplianceOfficer, PositiveCompliance, UNSCList, Company

User = get_user_model()

class UNSCListForm(ModelForm):
    class Meta:
        model = UNSCList
        fields = ['memo_name','memo_type','description','is_active']


class ComplianceForm(ModelForm):
    class Meta:
        model = Compliance
        #fields = '__all__'
        fields = ['match', 'information', 'is_complete']

class PositiveComplianceForm(ModelForm):
    class Meta:
        model = PositiveCompliance
        #fields = '__all__'        
        fields = ['unsc_reference_number','list_type','list_name_1','list_name_2',
                    'list_name_3','action','information','is_complete']

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['company_name','company_type','address_line_1','address_line_2',
                    'city','country','regulator','is_active']

class CreateComplianceOfficer(ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name', 'business_name','work_number', 'cellphone_number']

