from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.db.models import constraints, fields
from django.urls import reverse
from datetime import datetime
#from notification.models import Notification



# Create your models here.

class User(AbstractUser):
   is_regulator = models.BooleanField(default=False)
   is_officer = models.BooleanField(default=True)
   work_number = models.CharField(max_length=64, default=3650000)
   cellphone_number = models.CharField(max_length=64, default=72000000)
   business_name = models.ForeignKey('Company', null=True, on_delete=SET_NULL)
  

class UNSCType(models.Model):
    TYPES = [
        ('Santions List', 'Santions List'),
        ('Recommendations', 'Recommendations'),
        ('Memorandum','Memorandum')
    ]

    memo_type = models.CharField(max_length=64, choices=TYPES, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.memo_type


class UNSCList(models.Model):

    memo_name = models.CharField(max_length=255, db_index=True)
    memo_type = models.ForeignKey(UNSCType, null=True, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=False, auto_now_add=False)
    is_active = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

       
    class Meta:
        verbose_name_plural = 'UNSCLists'
    
    def __str__(self):
        return self.memo_name
    
        # def get_absolute_url(self):
        #    return reverse("_detail", kwargs={"pk": self.pk})
'''
def post_sanction_create_notification(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            Notification.objects.create(memo=instance, notification_type = 'INDVIVIDUAL', to_user=user,
                message=f'Sanction {instance.memo_name} has been created.  Please login to comply')

post_save.connect(post_sanction_create_notification, sender=UNSCList)   
'''

class Regulator(models.Model):

    REG = [
        ('NBFIRA', 'NBFIRA'),
        ('BICA', 'BICA'),
        ('FIA','FIA'),
        ('Other','Other'),
    ]

    regulator = models.CharField(max_length=64, choices=REG, unique=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.regulator


class CompanyType(models.Model):

    TYPES = [
        ('Bank', 'Bank'),
        ('Micro Lender', 'Micro Lender'),
        ('Insurer','Insurer'),
        ('Asset Management','Asset Management'),
        ('Lawyers','Lawyers')
    ]

    company_type = models.CharField(max_length=64, choices=TYPES, unique=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_type


class Company(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    company_type = models.ForeignKey(CompanyType, null=True, on_delete=models.SET_NULL)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    regulator = models.ManyToManyField(Regulator)
    slug = models.SlugField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = 'Companies'


class UNSCMemoTableFunction(models.Model):
    memo = models.ForeignKey(UNSCList, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=False, null=True, blank=True)
    memo_type = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_exist = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['memo','company'], name='possible_memo_per_company')]
    
    def __str__(self):
        return self.memo.memo_name + ' ' + self.company.company_name


def post_sanction_created_signal(sender, instance, created, **kwargs):
    if created:
        for company in Company.objects.all():
            UNSCMemoTableFunction.objects.create(memo=instance, memo_type = instance.memo_type, company=company)

post_save.connect(post_sanction_created_signal, sender=UNSCList)


class ComplianceOfficer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='power_user', on_delete=models.SET_NULL, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
   
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Compliance Officers'

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        ComplianceOfficer.objects.create(user=instance, company=instance.business_name, is_active=True)

post_save.connect(post_user_created_signal, sender=User)


class Compliance(models.Model):
    MATCH = [
        ('Positive_Match', 'Positive_Match'),
        ('Possible_Match', 'Possible_Match'),
        ('Negative_Match','Negative_Match'),
        ('Other','Other'),]
    memo_name = models.ForeignKey(UNSCList, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    officer = models.ForeignKey(ComplianceOfficer, null=True, on_delete=models.SET_NULL)
    update_date = models.DateTimeField(auto_now=True)
    match = models.CharField(max_length=64, choices=MATCH) 
    information = models.TextField()
    is_complete = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['memo_name','company'], name='one_memo_per_company')]

    def __str__(self):
        return self.memo_name.memo_name + ' ' + self.company.company_name
    
    
    #def get_absolute_url(self):
    #    return reverse('unsc:compliance', kwargs={"pk": self.pk})
    


class PositiveCompliance(models.Model):
    ACTION = [
        ('Freeze_Individual', 'Freeze_Individual'),
        ('Freeze_Entity', 'Freeze_Entity'),
        ('Delist_Individual','Delist_Individual'),
        ('Delist_Entity','Delist_Entity')
    ]

    TYPE = [
        ('Individual', 'Individual'),
        ('Entity', 'Entity'),
        ('Other','Other'),
    ]
    compliance = models.ForeignKey(Compliance, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    officer = models.ForeignKey(ComplianceOfficer, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    unsc_reference_number = models.CharField(max_length=50)
    list_type = models.CharField(max_length=64, choices=TYPE)
    list_name_1 = models.CharField(max_length=255)
    list_name_2 = models.CharField(max_length=255)
    list_name_3 = models.CharField(max_length=255)
    action = models.CharField(max_length=64, choices=ACTION) 
    information = models.TextField()
    is_complete = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['compliance','company', 'unsc_reference_number'], 
                        name='one_positive_compliance_reference_company')]

    def __str__(self):
        return str(self.compliance.memo_name) + ' ' + self.company.company_name
    
    def get_absolute_url(self):
        return reverse('unsc:positive', args={self.compliance.id})