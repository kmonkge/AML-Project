
import django_filters
from .models import *
from django_filters import DateFilter, CharFilter


class ComplianceFilter(django_filters.FilterSet):
    class Meta:
        model = Compliance
        fields = '__all__'