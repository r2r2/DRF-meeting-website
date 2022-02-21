from django.contrib.gis.measure import D
from django_filters import rest_framework
from rest_framework import filters

from dates.models import User


# class CustomSearchFilter(filters.SearchFilter):
#     def get_search_fields(self, view, request):
#         if request.GET.get('distance'):
#             return ['distance']


class ClientFilter(rest_framework.FilterSet):
    """Filtering list of clients"""

    class Meta:
        model = User
        fields = ('gender', 'first_name', 'last_name')


