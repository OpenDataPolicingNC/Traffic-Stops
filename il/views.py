from .models import Agency
from . import forms

from traffic_stops import base_views


class Home(base_views.Home):
    form_class = forms.AgencySearchForm
    template_name = 'il.html'
    success_url = 'il:agency-detail'


class AgencyList(base_views.AgencyList):
    model = Agency
    form_class = forms.AgencySearchForm
    success_url = 'il:agency-detail'
