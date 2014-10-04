from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Count
from stops.models import Stop, Agency
from stops import forms


def home(request):
    if request.method == 'POST':
        form = forms.AgencySearchForm(request.POST)
        if form.is_valid():
            agency = form.cleaned_data['agency']
            return redirect('agency-detail', agency.pk)
    else:
        form = forms.AgencySearchForm()
    context = {'agency_form': form}
    return render(request, 'home.html', context)


def search(request):
    query = None
    if request.method == 'GET':
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            query = form.get_query()
    else:
        form = forms.SearchForm()

    if query:
        stops = Stop.objects.filter(query)
    else:
        stops = Stop.objects.none()
    stops = stops.order_by('-date')
    context = {
        'form': form,
        'stops': stops,
    }
    return render(request, 'stops/search.html', context)


class AgencyList(ListView):
    model = Agency


class AgencyDetail(DetailView):
    model = Agency

    def get_context_data(self, **kwargs):
        context = super(AgencyDetail, self).get_context_data(**kwargs)
        agency = context['object']
        officers = Stop.objects.filter(agency=agency).values('officer_id')
        officers = officers.annotate(total_stops=Count('officer_id'))
        context['officers'] = officers.order_by('-total_stops')
        return context
