from django.shortcuts import render
from .models import Stop, Agency
from . import forms
from traffic_stops import base_views


class Home(base_views.Home):
    form_class = forms.AgencySearchForm
    template_name = 'md.html'
    success_url = 'md:agency-detail'


def search(request):
    if request.method == 'GET' and request.GET:
        form = forms.SearchForm(request.GET)
    else:
        form = forms.SearchForm()

    context = {
        'form': form,
    }
    return render(request, 'md/search.html', context)


class AgencyList(base_views.AgencyList):
    model = Agency
    form_class = forms.AgencySearchForm
    success_url = 'md:agency-detail'


class AgencyDetail(base_views.AgencyDetail):
    model = Agency
    stop_model = Stop
