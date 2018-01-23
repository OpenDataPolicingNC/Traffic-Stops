from django.conf import settings
from django.db import connections
from django.db.models import Count, Q

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultObjectKeyConstructor

from nc.models import Agency, Stop
from nc import serializers
from tsdata.utils import GroupedData


GROUPS = {'A': 'asian',
          'B': 'black',
          'I': 'native_american',
          'U': 'other',
          'W': 'white',
          'H': 'hispanic'}

PURPOSE_CHOICES = {1: 'Speed Limit Violation',
                   2: 'Stop Light/Sign Violation',
                   3: 'Driving While Impaired',
                   4: 'Safe Movement Violation',
                   5: 'Vehicle Equipment Violation',
                   6: 'Vehicle Regulatory Violation',
                   7: 'Seat Belt Violation',
                   8: 'Investigation',
                   9: 'Other Motor Vehicle Violation',
                   10: 'Checkpoint'}

GROUP_DEFAULTS = {'asian': 0,
                  'black': 0,
                  'native_american': 0,
                  'other': 0,
                  'white': 0,
                  'hispanic': 0}


class QueryKeyConstructor(DefaultObjectKeyConstructor):
    params_query = bits.QueryParamsKeyBit(['officer'])


query_cache_key_func = QueryKeyConstructor()


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = serializers.AgencySerializer

    def query(self, results, group_by, filter_=None):
        # date trunc on year, respecting NC time zone
        year_sql, year_params = connections[Stop.objects.db].ops.datetime_trunc_sql(
            'year', 'date', settings.NC_TIME_ZONE,
        )
        qs = Stop.objects.extra(select={'year': year_sql}, select_params=year_params)
        # filter down stops by agency only those who were drivers
        qs = qs.filter(agency=self.get_object(), person__type='D')
        # filter down by officer if supplied
        officer = self.request.query_params.get('officer', None)
        if officer:
            qs = qs.filter(officer_id=officer)
        if filter_:
            qs = qs.filter(filter_)
        # group by specified fields and order by year
        qs = qs.values(*group_by).order_by('year')
        for stop in qs.annotate(count=Count('date')):
            data = {}
            if 'year' in group_by:
                data['year'] = stop['year'].year
            if 'purpose' in group_by:
                purpose = PURPOSE_CHOICES.get(stop['purpose'],
                                              stop['purpose'])
                data['purpose'] = purpose

            if 'person__ethnicity' in group_by and stop['person__ethnicity'] == 'H':
                # The 'Hispanic' ethnicity option is now being aggreggated into its
                # own race category, and its count excluded from the other counts.
                race = GROUPS.get('H', 'H')
                data[race] = stop['count']
            elif 'person__race' in group_by:
                race = GROUPS.get(stop['person__race'],
                                  stop['person__race'])
                data.setdefault(race, 0)
                data[race] += stop['count']
            results.add(**data)

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def stops(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('year', 'person__race', 'person__ethnicity'))
        return Response(results.flatten())

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def stops_by_reason(self, request, pk=None):
        response = {}
        # stops
        results = GroupedData(by=('purpose', 'year'), defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('purpose', 'year', 'person__race', 'person__ethnicity'))
        response['stops'] = results.flatten()
        # searches
        results = GroupedData(by=('purpose', 'year'), defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('purpose', 'year', 'person__race', 'person__ethnicity'),
                   filter_=Q(search__isnull=False))
        response['searches'] = results.flatten()
        return Response(response)

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def use_of_force(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(search__isnull=False) & Q(engage_force='t')
        self.query(results, group_by=('year', 'person__race', 'person__ethnicity'), filter_=q)
        return Response(results.flatten())

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def searches(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(search__isnull=False)
        self.query(results, group_by=('year', 'person__race', 'person__ethnicity'), filter_=q)
        return Response(results.flatten())

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def contraband_hit_rate(self, request, pk=None):
        response = {}
        # searches
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(search__isnull=False)
        self.query(results, group_by=('year', 'person__race', 'person__ethnicity'), filter_=q)
        response['searches'] = results.flatten()
        # searches
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(search__contraband__isnull=False)
        self.query(results, group_by=('year', 'person__race', 'person__ethnicity'), filter_=q)
        response['contraband'] = results.flatten()
        return Response(response)
