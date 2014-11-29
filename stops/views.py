from django.shortcuts import render, redirect, Http404
from django.views.generic import ListView, DetailView
from django.db.models import Count
from stops.models import Stop, Agency, Person
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
    people = people.select_related('stop').order_by('-stop__date')
    context = {
        'form': form,
        'people': people,
    }
    return render(request, 'stops/search.html', context)


class AgencyList(ListView):
    model = Agency


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
        else:
            officers = Stop.objects.filter(agency=agency).values('officer_id')
            officers = officers.annotate(total_stops=Count('officer_id'))
            context['officers'] = officers.order_by('-total_stops')

        return context
