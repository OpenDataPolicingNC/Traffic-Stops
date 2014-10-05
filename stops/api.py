from collections import defaultdict

from django.db import connections
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from stops.models import Agency, Stop
from stops import serializers


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = serializers.AgencySerializer

    @detail_route(methods=['get'])
    def stops(self, request, pk=None):
        agency = self.get_object()
        year = connections[Stop.objects.db].ops.date_trunc_sql('year', 'date')
        stops = Stop.objects.filter(agency=agency, person__type='D')
        stops = stops.extra(select={'year': year}).values('year',
                                                          'person__race')
        data = defaultdict(dict)
        for stop in stops.annotate(count=Count('date')):
            data[stop['year'].year][stop['person__race']] = stop['count']
        response = []
        for year, stops in data.items():
            row = {'year': year}
            row.update(stops)
            response.append(row)
        return Response(response)

    @detail_route(methods=['get'])
    def stops_by_reason(self, request, pk=None):
        agency = self.get_object()
        stops = Stop.objects.filter(agency=agency, person__type='D')
        stops = stops.values('purpose', 'person__race')
        data = defaultdict(dict)
        for stop in stops.annotate(count=Count('purpose')):
            data[stop['purpose']][stop['person__race']] = stop['count']
        response = []
        for purpose, stops in data.items():
            row = {'purpose': purpose}
            row.update(stops)
            response.append(row)
        return Response(response)
