from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from stops.models import Stop, Agency
from stops import forms


def search(request):
    query = None
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            query = form.get_query()
    else:
        form = forms.SearchForm()

    if query:
        stops = Stop.objects.filter(query)
    else:
        stops = Stop.objects.none()
    stops = stops.order_by('-date')[:20]
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
