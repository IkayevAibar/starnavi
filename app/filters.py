
import django_filters
from .models import Like

class DateFilter(django_filters.FilterSet):
    date_from = django_filters.DateTimeFilter('created_at', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter('created_at', lookup_expr='lte')

    class Meta:
        model = Like
        fields = ['created_at'] 
