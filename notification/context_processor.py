
#from django.shortcuts import get_object_or_404
from .models import Notification
#from unsc.models import ComplianceOfficer, Company

def notifications(request):
    if request.user.is_authenticated:
        return {'notifications': request.user.to_user.filter(is_read=False)}
    else:
        return {'notifications': []}

#def company(request):
 #   if request.user.is_authenticated:
  #      my_user = get_object_or_404(ComplianceOfficer,  user=request.user)
   #     print('my user is :', my_user)
    #    company = get_object_or_404(Company, company_name=my_user.company)  
     #   print('my company name is :', company.slug)
      #  return {'company':company}
    
