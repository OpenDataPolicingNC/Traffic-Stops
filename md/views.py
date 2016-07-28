from django.shortcuts import render, redirect, Http404
from django.views.generic import ListView, DetailView, View, TemplateView
from .models import Stop, Agency
from . import forms
import math


def home(request):
    if request.method == 'GET' and request.GET:
        form = forms.AgencySearchForm(request.GET)
        if form.is_valid():
            agency = form.cleaned_data['agency']
            return redirect('md:agency-detail', agency.pk)
    else:
        form = forms.AgencySearchForm()
    context = {'agency_form': form}
    return render(request, 'md.html', context)


def search(request):
    if request.method == 'GET' and request.GET:
        form = forms.SearchForm(request.GET)
    else:
        form = forms.SearchForm()

    context = {
        'form': form,
    }
    return render(request, 'md/search.html', context)


def get_chunks(xs, chunk_count=3):
    """
    Helper function to split a list into roughly equally sized chunks.
    """
    chunk_width = math.ceil(len(xs) / chunk_count)
    ranges = range(0, len(xs), chunk_width)
    return [xs[x:x + chunk_width] for x in ranges]


class AgencyList(ListView):
    model = Agency

    def get_context_data(self, **kwargs):
        context = super(AgencyList, self).get_context_data(**kwargs)

        if self.request.method == 'GET' and self.request.GET:
            form = forms.AgencySearchForm(request.GET)
            if form.is_valid():
                agency = form.cleaned_data['agency']
                return redirect('md:agency-detail', agency.pk)
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
