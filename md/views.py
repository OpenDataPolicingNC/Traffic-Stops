from django.shortcuts import render, redirect, Http404
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import ProcessFormView, FormMixin
from .models import Stop, Agency
from . import forms
from traffic_stops.utils import get_chunks
from collections import defaultdict


class Home(FormMixin, ProcessFormView, TemplateView):
    form_class = forms.AgencySearchForm
    template_name = 'md.html'

    def get(self, request, *args, **kwargs):
        if request.GET:
            form = self.get_form_class()(request.GET)
            if form.is_valid():
                return redirect('md:agency-detail', form.cleaned_data['agency'].pk)
        return super(Home, self).get(request, **kwargs)


def search(request):
    if request.method == 'GET' and request.GET:
        form = forms.SearchForm(request.GET)
    else:
        form = forms.SearchForm()

    context = {
        'form': form,
    }
    return render(request, 'md/search.html', context)


class AgencyList(FormMixin, ListView):
    model = Agency
    form_class = forms.AgencySearchForm
    success_url = 'md:agency-detail'

    def get_success_url(self, pk, **kwargs):
        success = self.get_success_url()
        return redirect(success, pk)

    def get(self, request, **kwargs):
        if request.GET:
            form = self.get_form_class()(request.GET)
            if form.is_valid():
                return self.get_success_url(pk=form.cleaned_data['agency'].pk)
        return super(AgencyList, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AgencyList, self).get_context_data(**kwargs)

        # The following seems to be all ProcessFormView really gives us.
        # It causes collisions with ListView's get method. Hence
        # we just add it as a trivial context-modification snippet.
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form

        # Once we have the "letters present", we want to be able to iterate
        # over categorized, sorted lists of agencies. Therefore we create
        # a dict indexed by first letter.
        sorted_agencies = defaultdict(list)

        for agency in context['agency_list']:
            initial = agency.name[:1]
            sorted_agencies[initial].append(agency)

        for key in sorted_agencies:
            sorted_agencies[key].sort(key=lambda x: x.name)
            sorted_agencies[key] = get_chunks(sorted_agencies[key])

        sorted_agencies = sorted(sorted_agencies.items())

        context['sorted_agencies'] = sorted_agencies
        context['agency_form'] = form

        return context


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
