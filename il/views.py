from .models import Agency, Stop
from . import forms

from traffic_stops import base_views


class Home(base_views.Home):
    form_class = forms.AgencySearchForm
    template_name = 'il.html'
    success_url = 'il:agency-detail'


class AgencyDetail(base_views.AgencyDetail):
    model = Agency
    stop_model = Stop


class AgencyList(base_views.AgencyList):
    model = Agency
    form_class = forms.AgencySearchForm
    success_url = 'il:agency-detail'
