from collections import defaultdict, OrderedDict

from django.db import connections
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from stops.models import Agency, Stop, Person
from stops import serializers
from stops.utils import GroupedData

from pprint import pprint


GROUPS = {'A': 'asian',
          'B': 'black',
          'I': 'native_american',
          'U': 'other',
          'W': 'white',
          'H': 'hispanic',
          'N': 'non-hispanic'}

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

    def query(self, results, group_by):
        # date trunc on year
        year = connections[Stop.objects.db].ops.date_trunc_sql('year', 'date')
        qs = Stop.objects.extra(select={'year': year})
        # filter down stops by agency only those who were drivers
        qs = qs.filter(agency=self.get_object(), person__type='D')
        # group by specified fields and order by year
        qs = qs.values(*group_by).order_by('year')
        for stop in qs.annotate(count=Count('date')):
            data = {}
            if 'person__race' in group_by:
                race = GROUPS.get(stop['person__race'],
                                  stop['person__race'])
                data = {race: stop['count']}
            if 'person__ethnicity' in group_by:
                ethnicity = GROUPS.get(stop['person__ethnicity'],
                                       stop['person__ethnicity'])
                data = {ethnicity: stop['count']}
            group = []
            for name in results.group_by:
                value = stop[name]
                if name == 'year':
                    value = value.year
                group.append(value)
            results.add(*group, **data)

    @detail_route(methods=['get'])
    def stops(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('year', 'person__race'))
        self.query(results, group_by=('year', 'person__ethnicity'))
        return Response(results.flatten())

    @detail_route(methods=['get'])
    def stops_by_reason(self, request, pk=None):
        query = self.years().filter(agency=self.get_object(), person__type='D')
        query = query.values('purpose', 'year', 'person__race').order_by('year')
        stops = GroupedData(by=('purpose', 'year'), defaults=GROUP_DEFAULTS)
        for stop in query.annotate(count=Count('person')):
            race = GROUPS.get(stop['person__race'], stop['person__race'])
            data = {race: stop['count']}
            stops.add(stop['purpose'], stop['year'].year, **data)
        query = self.years().filter(agency=self.get_object(), person__type='D')
        query = query.values('purpose', 'year', 'person__ethnicity').order_by('year')
        for stop in query.annotate(count=Count('date')):
            race = GROUPS.get(stop['person__ethnicity'],
                              stop['person__ethnicity'])
            data = {race: stop['count']}
            stops.add(stop['year'].year, **data)
        return Response(stops.flatten())
