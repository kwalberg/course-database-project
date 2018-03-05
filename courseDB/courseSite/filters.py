from .models import Course
import django_filters

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Course
        fields = ['title', 'instructor', 'description']