from django.db.models import fields
from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, UNSCList, Regulator, UNSCType, CompanyType, Compliance, ComplianceOfficer, User, UNSCMemoTableFunction
from .forms import ComplianceForm, CreateCompanyForm, CreateComplianceOfficer, PositiveComplianceForm, UNSCListForm
from .filters import *
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from urllib.parse import urlencode
from notification.views import create_notification
from django.utils.text import slugify
import datetime
from collections import Counter
from django.http import JsonResponse, request
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def company_processor(request):
    if request.user.is_authenticated:
        my_user = get_object_or_404(ComplianceOfficer,  user=request.user)
        #print('my user is :', my_user)
        user_company = get_object_or_404(Company, company_name=my_user.company)  
        #print('my company name is :', user_company.slug)
        return {'user_company':user_company}
    else:
        user_company = get_object_or_404(Company, company_name='Credit Check')
        return {'user_company':user_company}
@login_required(login_url='/login/')
def index(request):
    companies = Company.objects.all()
    context ={}
    return render(request, 'unsc/index.html', context)

@login_required(login_url='/login/')
def home(request):
    if request.user.is_authenticated and request.user.is_officer:
        my_user = get_object_or_404(ComplianceOfficer,  user=request.user)
        user_company = get_object_or_404(Company, company_name=my_user.company)
        context =  {'user_company':user_company} 
        return redirect ('unsc:company', slug=user_company.slug)
    else:
        if request.user.is_authenticated and request.user.is_regulator:
            return redirect ('unsc:dashboard')




@login_required(login_url='/login/')
def regulator_dashboard(request):
    company = Company.objects.filter(is_active=True)
    comp_sanctions = UNSCMemoTableFunction.objects.all()
    comp_comply = Compliance.objects.all()
    comp_positive = PositiveCompliance.objects.all()
    sanctions = UNSCList.objects.filter(is_active=True)
    

    exist_sanc = comp_sanctions.all().values_list('is_exist')
    #no_exist = comp_sanctions.filter(is_exist=False).values_list('memo__memo_name', 'company__company_name')
    no_exist = comp_sanctions.filter(is_exist=False)

    positive_matches = comp_comply.filter(is_complete=True, match='Positive_Match').values_list('company__company_name', 'match')
    negative_matches = comp_comply.filter(is_complete=True, match='Negative_Match').values_list('company__company_name', 'match')


    positive_match_count_company = Counter([p[0] for p in positive_matches])
    negative_match_count_company = Counter([n[0] for n in negative_matches])
    exist_count = Counter([e[0] for e in exist_sanc])
    
    comp_per = round((exist_count[True]/(exist_count[False]+exist_count[True]))*100,1)
    non_comp_per = round((exist_count[False]/(exist_count[False]+exist_count[True]))*100,2)
    
    compliant = f'Compliant {comp_per} %'
    non_compliant = f'Non Compliant {non_comp_per} %'
    exist_count[compliant] = exist_count.pop(True)
    exist_count[non_compliant] = exist_count.pop(False)


    neg_data= dict(negative_match_count_company)
    pos_data = dict(positive_match_count_company)
    exist_data = dict(exist_count)
    no_of_comp = len(company)
    no_of_sanctions  =len(sanctions)
   
    #print('Exiting sanctions:', exist_sanc)
    #print('exist count data:', exist_count)
    #print('exist is False:', no_exist)


    context = {'company': company, 'comp_sanctions': comp_sanctions, 
                'comp_comply': comp_comply, 'comp_positive': comp_positive, 'neg_data':neg_data, 'pos_data':pos_data, 'exist_data': exist_data, 
                'comp_per':comp_per,'non_comp_per':non_comp_per, 'no_comp':no_of_comp, 'no_sanctions':no_of_sanctions, 'no_exist':no_exist }

    return render(request, 'unsc/dashboard.html', context)    


@login_required(login_url='/login/')
def company_dashboard(request, slug):
    company = get_object_or_404(Company, slug=slug, is_active=True)

    comp_sanctions = UNSCMemoTableFunction.objects.filter(company__slug=slug)
    comp_comply = Compliance.objects.filter(company=company.id)
    comp_positive = PositiveCompliance.objects.filter(company=company.id)
    

    exist_sanc = comp_sanctions.all().values_list('is_exist')
    #no_exist = comp_sanctions.filter(is_exist=False).values_list('memo__memo_name', 'company__company_name')
    no_exist = comp_sanctions.filter(is_exist=False)
    print('No exist', no_exist)
    for n in no_exist:
        print('This is slug for above:', n.slug)
    

    positive_matches = comp_comply.filter(is_complete=True, match='Positive_Match').values_list('company__company_name', 'match')
    negative_matches = comp_comply.filter(is_complete=True, match='Negative_Match').values_list('company__company_name', 'match')


    positive_match_count_company = Counter([p[0] for p in positive_matches])
    negative_match_count_company = Counter([n[0] for n in negative_matches])
    exist_count = Counter([e[0] for e in exist_sanc])
    #print('Exist Count:',exist_count)
    if len(exist_count):
        comp_per = round((exist_count[True]/(exist_count[False]+exist_count[True]))*100,1)
        non_comp_per = round((exist_count[False]/(exist_count[False]+exist_count[True]))*100,2)
    
        compliant = f'Compliant {comp_per} %'
        non_compliant = f'Non Compliant {non_comp_per} %'

        if 'True' in exist_count:
            exist_count[compliant] = exist_count.pop(True)
        if 'False' in exist_count:
            exist_count[non_compliant] = exist_count.pop(False)
  


    neg_data= dict(negative_match_count_company)
    pos_data = dict(positive_match_count_company)
    exist_data = dict(exist_count)
    no_of_sanction = len(comp_sanctions)
  

    # Search Function
    #myfilter = ComplianceFilter(request.GET, queryset=company_comp )

    context = {'company': company, 'comp_sanctions': comp_sanctions, 
                'comp_comply': comp_comply, 'comp_positive': comp_positive, 'neg_data':neg_data, 'pos_data':pos_data, 'exist_data': exist_data, 
                'comp_per':comp_per,'non_comp_per':non_comp_per,  'no_exist':no_exist, 'no_of_sanctions':no_of_sanction }

    
    return render(request, 'unsc/dashboard_comp.html', context)


@login_required(login_url='/login/')
def createSanction(request):
    sanction_form = UNSCListForm

    if request.method == 'POST':
        sanction_form = UNSCListForm(request.POST)
        if sanction_form.is_valid:
            sanction = sanction_form.save(commit=False)
            sanction.created_by = request.user
            sanction.slug = slugify(sanction.memo_name)
            sanction.save()
            notification = f'sanction {sanction.memo_name} has been created.  Please acknowledge receipt by completing the compliance request'
            print('I have saved the sanction object and created the message')
            for user in User.objects.all().exclude(username='admin', is_regulator=True):
                create_notification(request, to_user=user, notification_type='INDIVIDUAL', extra_id=sanction.slug, message=notification, created_by=request.user)
            return redirect('unsc:dashboard')

    context = {'sanction_form': sanction_form}
    return render(request, 'unsc/sanctions.html', context)



class SanctionsListView(LoginRequiredMixin, ListView):
    template_name = 'unsc/sanctionsList.html'
    # context named as: context={'object_list': UNSCList} therefore rename
    queryset = UNSCList.objects.all()
    context_object_name = 'sanctions'



class SanctionsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'unsc/sanctionsUpdate.html'
    queryset = UNSCList.objects.all()
    form_class = UNSCListForm
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('unsc:sanction-list')


#@login_required(login_url='/login/')
def createCompliance(request, slug1, slug2):
    name = get_object_or_404(UNSCList, slug=slug2)
    #name = get_object_or_404(UNSCMemoTableFunction, slug=slug2)
    comp = get_object_or_404(Company, slug=slug1)
    officer_name = get_object_or_404(ComplianceOfficer, company=comp.id)
    list_dbase = get_object_or_404(UNSCMemoTableFunction, slug=slug2, company=comp.id)
    print('This is objects:', list_dbase)

    c_form = ComplianceForm

    if request.method == 'POST':
        c_form = ComplianceForm(request.POST)
        
        if c_form.is_valid:
            record = c_form.save(commit=False)
            record.memo_name = name
            record.company = comp
            record.officer = officer_name
            record.created_by = request.user
            record.save()
            list_dbase.is_exist=True
            list_dbase.save(update_fields=['is_exist'])
            print('list base is_exist status', list_dbase.is_exist)
            print('Getting the form id:', record.id)
            print('The cleaned data is:', c_form.cleaned_data)
            data = c_form.cleaned_data.get('match')
            if (data == 'Positive Match' or data == 'Possible Match'):
                base_url = reverse('unsc:positive')
                query_string = urlencode({'pk': record.id})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
            return redirect('unsc:company', slug=slug1)

    context = {'c_form': c_form,}
    return render(request, 'unsc/create_compliance.html', context)

class ComplianceListView(ListView):
    #def get(self, request):
     #       business = request.user.business_name
      #      return business
    template_name = 'unsc/complianceList.html'
    # context named as: context={'object_list': UNSCList} therefore rename
    #business = request.user.business_name
    #queryset =Compliance.objects.all()
    context_object_name = 'compliance'
    
    def get_queryset(self):
        my_user = ComplianceOfficer.objects.get(user=self.request.user)
        print('my user is :', my_user)
        company = my_user.company
        print('my company name is :', company)
        return Compliance.objects.filter(company__company_name=company)
    


@login_required(login_url='/login/')
def updateCompliance(request, pk):
    comply = get_object_or_404(Compliance, id=pk)
    # comp = comply.company
    comp = get_object_or_404(Company, id=comply.company.id)
    form = ComplianceForm(instance=comply)
    print('company slug:', comp.slug)
    if request.method == 'POST':
        form = ComplianceForm(request.POST, instance=comply)
        if form.is_valid():
            form.save()
            return redirect('unsc:company', slug=comp.slug)
    
    context = {'form': form}
    return render(request, 'unsc/compliance.html', context)


@login_required(login_url='/login/')
def positiveCompliance(request):
    comply_id = request.GET.get('pk')
    compliance = get_object_or_404(Compliance, id=comply_id)
    slug1 = compliance.company.slug
    #slug1 = company.slug
    print('compliance is:', compliance)

    ComplianceFormSet = inlineformset_factory(Compliance, PositiveCompliance, fields=('unsc_reference_number',
                        'list_type','list_name_1','list_name_2', 'list_name_3','action', 
                        'information','is_complete'))


    form = ComplianceFormSet()

    if request.method == 'POST':
        print('have entered post method')
        
        form = ComplianceFormSet(request.POST)
        if form.is_valid():
            print('form is valid')
            record = form.save(commit=False)
            record.compliance = compliance
            record.company = compliance.company
            record.officer = compliance.officer
            record.created_by = request.user
            record.save()         
            return redirect('unsc:company', slug=slug1)
        else:
            print('There is an error')

    context= {'form': form}
    return render(request, 'unsc/positive_compliance.html', context)


class PositiveComplianceListView(LoginRequiredMixin, ListView):
    template_name = 'unsc/positiveComplianceList.html'
    # context named as: context={'object_list': UNSCList} therefore rename
    #queryset = PositiveCompliance.objects.all()
    context_object_name = 'compliance'

    def get_queryset(self):
        my_user = ComplianceOfficer.objects.get(user=self.request.user)
        print('my user is :', my_user)
        company = my_user.company
        print('my company name is :', company)
        return PositiveCompliance.objects.filter(company__company_name=company)
    


class PositiveComplianceUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'unsc/positiveComplianceUpdate.html'
    queryset = PositiveCompliance.objects.all()
    form_class = PositiveComplianceForm
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('unsc:positiveCompliance-list')


@login_required(login_url='/login/')
def create_company(request):
    company_form = CreateCompanyForm

    if request.method == 'POST':
        company_form = CreateCompanyForm(request.POST)
        if company_form.is_valid():
            form = company_form.save(commit=False)
            form.created_by = request.user
            form.slug=slugify(form.company_name)
            form.save()
            return redirect('unsc:dashboard')

    context = {'company_form': company_form}
    return render(request, 'unsc/create_company.html', context)


class CompanyListView(LoginRequiredMixin, ListView):
    template_name = 'unsc/companyList.html'
    # context named as: context={'object_list': UNSCList} therefore rename
    queryset = Company.objects.all()
    context_object_name = 'company'


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'unsc/companyUpdate.html'
    queryset = Company.objects.all()
    form_class = CreateCompanyForm
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('unsc:company-list')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def create_officer(request):
    officer_form = CreateComplianceOfficer
    if request.method == 'POST':
        officer_form = CreateComplianceOfficer(request.POST)
        if officer_form.is_valid():
            user = officer_form.save(commit=False)
            user.username = user.email
            user.is_regulator = False
            user.is_officer = True
            user.save()

            #ComplianceOfficer.objects.create(user=user, company=user.business_name, 
              #                                  created_by=request.user, is_active=True)

            return redirect('unsc:dashboard')

    context = {'officer_form': officer_form}
    return render(request, 'unsc/create_officer.html', context)

class ComplianceOfficerListView(LoginRequiredMixin, ListView):
    template_name = 'unsc/complianceOfficerList.html'
    # context named as: context={'object_list': UNSCList} therefore rename
    queryset = ComplianceOfficer.objects.all()
    context_object_name = 'compliance_officer'


class ComplianceOfficerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'unsc/complianceOfficerUpdate.html'
    queryset = ComplianceOfficer.objects.all()
    form_class = CreateComplianceOfficer
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('unsc:complianceOfficer-list')

