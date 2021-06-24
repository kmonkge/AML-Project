from collections import namedtuple
from django import urls
from notification import *
from django.urls import path
from django.urls.conf import include

import notification
from . import views


app_name = 'unsc'



urlpatterns = [
    #path('', views.index, name='index'),
    path('',views.home, name='home'),
    path('dashboard/', views.regulator_dashboard, name='dashboard'),
    path('dashboard/<slug:slug>/', views.company_dashboard, name='company'),
    #path('compliance/<slug:slug1>/<slug:slug2>/', views.compliance, name='complyForm'),
    path('createCompliance/<slug:slug1>/<slug:slug2>/', views.createCompliance, name='comply'),
    path('positiveCompliance/', views.positiveCompliance, name='positive'),
    path('update_compliance/<str:pk>/', views.updateCompliance, name='updateForm'),
    #path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logOutPage'),
    path('sanctions/', views.createSanction, name='sanctions'),
    path('createCompany/', views.create_company, name='create-company'),
    path('createOfficer/', views.create_officer, name='create-officer'),

    path('notifications/', notification.views.notification, name='notifications'),

    path('sanctionsList/', views.SanctionsListView.as_view(), name='sanction-list'),
    path('sanctionsUpdate/<int:pk>', views.SanctionsUpdateView.as_view(), name='sanction-update'),
    path('companyList/', views.CompanyListView.as_view(), name='company-list'),
    path('companyUpdate/<int:pk>', views.CompanyUpdateView.as_view(), name='company-update'),
    path('positiveComplianceList/', views.PositiveComplianceListView.as_view(), name='positiveCompliance-list'),
    path('positiveComplianceUpdate/<int:pk>', views.PositiveComplianceUpdateView.as_view(), name='positiveCompliance-update'),
    path('complianceOfficerList/', views.ComplianceOfficerListView.as_view(), name='complianceOfficer-list'),
    path('complianceOfficerUpdate/<int:pk>', views.ComplianceOfficerUpdateView.as_view(), name='complianceOfficer-update'),
    path('complianceList/', views.ComplianceListView.as_view(), name='compliance-list'),
    
]
