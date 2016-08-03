from django.shortcuts import render

from .models import Stop, Agency
from . import forms
from traffic_stops import base_views


class Home(base_views.Home):
    form_class = forms.AgencySearchForm
    template_name = 'md.html'
    success_url = 'md:agency-detail'


def search(request):
    query = None
    if request.method == 'GET' and request.GET:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            query = form.get_query()
    else:
        form = forms.SearchForm()

    if query:
        stops = Stop.objects.filter(query)
    else:
        stops = Stop.objects.none()
    context = {
        'form': form,
        'stops': stops,
    }
    return render(request, 'md/search.html', context)


class AgencyList(base_views.AgencyList):
    model = Agency
    form_class = forms.AgencySearchForm
    success_url = 'md:agency-detail'


class AgencyDetail(base_views.AgencyDetail):
    model = Agency
    stop_model = Stop
