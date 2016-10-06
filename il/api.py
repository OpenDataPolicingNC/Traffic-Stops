from django.db.models import Count, Q

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor.constructors import DefaultObjectKeyConstructor

from il.models import Agency, Stop
from il import serializers
from il.models import ETHNICITY_CHOICES, PURPOSE_CHOICES
from tsdata.utils import GroupedData


GROUP_DEFAULTS = {k: 0 for k in dict(ETHNICITY_CHOICES).values()}

query_cache_key_func = DefaultObjectKeyConstructor()


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = serializers.AgencySerializer

    def query(self, results, group_by, filter_=None):
        qs = Stop.objects.filter(agency=self.get_object())
        if filter_:
            qs = qs.filter(filter_)
        # group by specified fields and order by year
        qs = qs.values(*group_by).order_by('year')
        for stop in qs.annotate(count=Count('year')):
            data = {}
            if 'year' in group_by:
                data['year'] = stop['year']
            if 'purpose' in group_by:
                purpose = dict(PURPOSE_CHOICES).get(stop['purpose'],
                                                    stop['purpose'])
                data['purpose'] = purpose
            if 'ethnicity' in group_by:
                ethnicity = dict(ETHNICITY_CHOICES).get(stop['ethnicity'],
                                                        stop['ethnicity'])
                data[ethnicity] = stop['count']
            results.add(**data)

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def stops(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('year', 'ethnicity'))
        return Response(results.flatten())

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def stops_by_reason(self, request, pk=None):
        response = {}
        # stops
        results = GroupedData(by=('purpose', 'year'), defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('purpose', 'year', 'ethnicity'))
        response['stops'] = results.flatten()
        # searches
        results = GroupedData(by=('purpose', 'year'), defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('purpose', 'year', 'ethnicity'),
                   filter_=Q(search_conducted='Y'))
        response['searches'] = results.flatten()
        return Response(response)

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def searches(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(search_conducted='Y')
        self.query(results, group_by=('year', 'ethnicity'), filter_=q)
        return Response(results.flatten())

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def contraband_hit_rate(self, request, pk=None):
        response = {}
        # searches
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(search_conducted='Y')
        self.query(results, group_by=('year', 'ethnicity'), filter_=q)
        response['searches'] = results.flatten()
        # contraband
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(seized='Y')
        self.query(results, group_by=('year', 'ethnicity'), filter_=q)
        response['contraband'] = results.flatten()
        return Response(response)
