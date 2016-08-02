from django.shortcuts import render
from .models import Stop, Agency, Person
from . import forms
from traffic_stops import base_views


class Home(base_views.Home):
    form_class = forms.AgencySearchForm
    template_name = 'nc.html'
    success_url = 'nc:agency-detail'


def search(request):
    query = None
    if request.method == 'GET' and request.GET:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            query = form.get_query()
    else:
        form = forms.SearchForm()

    if query:
        people = Person.objects.filter(query)
    else:
        people = Person.objects.none()
    people = people.select_related('stop').order_by('stop__date')
    context = {
        'form': form,
        'people': people,
    }
    return render(request, 'nc/search.html', context)


class AgencyList(base_views.AgencyList):
    model = Agency
    form_class = forms.AgencySearchForm
    success_url = 'nc:agency-detail'


class AgencyDetail(base_views.AgencyDetail):
    model = Agency
    stop_model = Stop
