from django.shortcuts import get_object_or_404
from .models import ComplianceOfficer, Company


def company_processor(request):
    if request.user.is_authenticated:
        my_user = get_object_or_404(ComplianceOfficer,  user=request.user)
        print('my user is :', my_user)
        user_company = get_object_or_404(Company, company_name=my_user.company)  
        print('my company name is :', user_company.slug)
        return {'user_company':user_company}
    else:
        user_company = get_object_or_404(Company, company_name='Credit Check')
        return {'user_company':user_company}