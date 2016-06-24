from django.shortcuts import render, redirect, Http404
from django.views.generic import ListView, DetailView, View, TemplateView
from .models import Stop, Agency
from . import forms


def search(request):
    if request.method == 'GET' and request.GET:
        form = forms.SearchForm(request.GET)
    else:
        form = forms.SearchForm()

    context = {
        'form': form,
    }
    return render(request, 'md/search.html', context)


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

        return context
