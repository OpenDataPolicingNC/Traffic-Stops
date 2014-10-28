from django.db import connections
from django.db.models import Count, Q

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.utils import default_object_cache_key_func

from stops.models import Agency, Stop, Person
from stops import serializers
from stops.utils import GroupedData


GROUPS = {'A': 'asian',
          'B': 'black',
          'I': 'native_american',
          'U': 'other',
          'W': 'white',
          'H': 'hispanic',
          'N': 'non-hispanic'}

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
                  'hispanic': 0,
                  'non-hispanic': 0}


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = serializers.AgencySerializer

    def query(self, results, group_by, filter_=None):
        # date trunc on year
        year = connections[Stop.objects.db].ops.date_trunc_sql('year', 'date')
        qs = Stop.objects.extra(select={'year': year})
        # filter down stops by agency only those who were drivers
        qs = qs.filter(agency=self.get_object(), person__type='D')
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
            if 'person__race' in group_by:
                race = GROUPS.get(stop['person__race'],
                                  stop['person__race'])
                data[race] = stop['count']
            if 'person__ethnicity' in group_by:
                ethnicity = GROUPS.get(stop['person__ethnicity'],
                                       stop['person__ethnicity'])
                data[ethnicity] = stop['count']
            results.add(**data)

    @detail_route(methods=['get'])
    @cache_response(key_func=default_object_cache_key_func)
    def stops(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('year', 'person__race'))
        self.query(results, group_by=('year', 'person__ethnicity'))
        return Response(results.flatten())

    @detail_route(methods=['get'])
    @cache_response(key_func=default_object_cache_key_func)
    def stops_by_reason(self, request, pk=None):
        response = {}
        # stops
        results = GroupedData(by=('purpose', 'year'), defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('purpose', 'year', 'person__race'))
        self.query(results, group_by=('purpose', 'year', 'person__ethnicity'))
        response['stops'] = results.flatten()
        # searches
        results = GroupedData(by=('purpose', 'year'), defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('purpose', 'year', 'person__race'),
                   filter_=Q(search__isnull=False))
        self.query(results, group_by=('purpose', 'year', 'person__ethnicity'),
                   filter_=Q(search__isnull=False))
        response['searches'] = results.flatten()
        return Response(response)

    @detail_route(methods=['get'])
    @cache_response(key_func=default_object_cache_key_func)
    def use_of_force(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(search__isnull=False) & Q(engage_force='t')
        self.query(results, group_by=('year', 'person__race'), filter_=q)
        self.query(results, group_by=('year', 'person__ethnicity'), filter_=q)
        return Response(results.flatten())

    @detail_route(methods=['get'])
    @cache_response(key_func=default_object_cache_key_func)
    def searches(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        q = Q(search__isnull=False)
        self.query(results, group_by=('year', 'person__race'), filter_=q)
        self.query(results, group_by=('year', 'person__ethnicity'), filter_=q)
        return Response(results.flatten())
