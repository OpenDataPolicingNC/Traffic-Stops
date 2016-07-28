from django.shortcuts import render, redirect, Http404
from django.views.generic import ListView, DetailView
from .models import Stop, Agency, Person
from . import forms
from traffic_stops.utils import get_chunks


def home(request):
    if request.method == 'GET' and request.GET:
        form = forms.AgencySearchForm(request.GET)
        if form.is_valid():
            agency = form.cleaned_data['agency']
            return redirect('nc:agency-detail', agency.pk)
    else:
        form = forms.AgencySearchForm()
    context = {'agency_form': form}
    return render(request, 'nc.html', context)


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


class AgencyList(ListView):
    model = Agency

    def get_context_data(self, **kwargs):
        context = super(AgencyList, self).get_context_data(**kwargs)

        if self.request.method == 'GET' and self.request.GET:
            form = forms.AgencySearchForm(self.request.GET)
            if form.is_valid():
                agency = form.cleaned_data['agency']
                return redirect('nc:agency-detail', agency.pk)
        else:
            form = forms.AgencySearchForm()

        # Once we have the "letters present", we want to be able to iterate
        # over categorized, sorted lists of agencies. Therefore we create
        # a dict indexed by first letter.
        sorted_agencies = {}

        for agency in context['agency_list']:
            initial = agency.name[:1]
            if initial not in sorted_agencies:
                sorted_agencies[initial] = []
            sorted_agencies[initial].append(agency)

        for key in sorted_agencies:
            sorted_agencies[key].sort(key=lambda x: x.name)
            sorted_agencies[key] = get_chunks(sorted_agencies[key])

        sorted_agencies = sorted(sorted_agencies.items())

        return dict(context, **{"sorted_agencies": sorted_agencies,
                                "agency_form": form, })


class AgencyDetail(DetailView):
    model = Agency

    def get_context_data(self, **kwargs):
        context = super(AgencyDetail, self).get_context_data(**kwargs)
        agency = context['object']
        officer_id = self.request.GET.get('officer_id')

        if officer_id:
            if not Stop.objects.filter(agency=agency, officer_id=officer_id).exists():
                raise Http404()
            context['officer_id'] = officer_id

        return context
