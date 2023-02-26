from rest_framework import generics
from django_filters import rest_framework as filters
from lianjia.models import House


class HouseDetailFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    max_size = filters.NumberFilter(field_name='size', lookup_expr='lte')
    min_size = filters.NumberFilter(field_name='size', lookup_expr='gte')

    class Meta:
        model = House
        fields = ['min_price', 'max_price', 'max_size', 'min_size', 'decorate', 'use']
