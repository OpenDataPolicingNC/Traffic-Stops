from django.shortcuts import render
from stops.models import Stop

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
        stops = Stop.objects.filter(query)[:20]
    else:
        stops = None
    # if stops:
    #     stops = stops.order_by('-date')
    context = {
        'form': form,
        'stops': stops,
    }
    return render(request, 'stops/search.html', context)
