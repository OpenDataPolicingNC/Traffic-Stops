from django.db import connections
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultObjectKeyConstructor

from md.models import Agency, Stop
from md import serializers
from tsdata.utils import GroupedData


GROUPS = {'A': 'ASIAN',
          'B': 'BLACK',
          'I': 'NATIVE AMERICAN',
          'U': 'UNKNOWN',
          'W': 'WHITE',
          'H': 'HISPANIC'}

# PURPOSE_CHOICES to be added after ODPM-31

GROUP_DEFAULTS = {'ASIAN': 0,
                  'BLACK': 0,
                  'NATIVE AMERICAN': 0,
                  'UNKNOWN': 0,
                  'WHITE': 0,
                  'HISPANIC': 0,
                  }


class QueryKeyConstructor(DefaultObjectKeyConstructor):
    params_query = bits.QueryParamsKeyBit(['officer'])

query_cache_key_func = QueryKeyConstructor()


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = serializers.AgencySerializer

    def query(self, results, group_by, filter_=None):
        # date trunc on year
        year = connections[Stop.objects.db].ops.date_trunc_sql('year', 'date')
        qs = Stop.objects.extra(select={'year': year})
        qs = qs.filter(agency=self.get_object())
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
            # XXX check for 'purpose' here after ODPM-31 is delivered.
            if 'ethnicity' in group_by:
                ethnicity = GROUPS.get(stop['ethnicity'],
                                       stop['ethnicity'])
                data[ethnicity] = stop['count']
            results.add(**data)

    @detail_route(methods=['get'])
    @cache_response(key_func=query_cache_key_func)
    def stops(self, request, pk=None):
        results = GroupedData(by='year', defaults=GROUP_DEFAULTS)
        self.query(results, group_by=('year', 'ethnicity'))
        return Response(results.flatten())

    # for additional methods related to searches, look first at most recent
    # corresponding nc code