from django.shortcuts import render

from stops import forms


def search(request):
    form = forms.SearchForm()
    context = {
        'form': form,
    }
    return render(request, 'stops/search.html', context)
