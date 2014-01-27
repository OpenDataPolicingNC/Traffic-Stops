from django.shortcuts import render
from django.views.generic import ListView, DetailView
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
