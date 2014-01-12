from selectable.base import ModelLookup
from selectable.registry import registry

from stops.models import Stop


class AgencyLookup(ModelLookup):
    model = Stop
    search_fields = (
        'agency_description__icontains',
    )

    # def get_query(self, request, term):
    #     data = ['Foo', 'Bar']
    #     return filter(lambda x: x.startswith(term), data)

registry.register(AgencyLookup)
