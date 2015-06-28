from django.shortcuts import render, redirect, Http404
from django.views.generic import ListView, DetailView, View
from django.db.models import Count
from django.http import HttpResponse, HttpResponseNotAllowed
from nc.models import Stop, Agency, Person
from nc import forms


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


class UpdateSession(View):

    http_method_names = (u'post', )

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseNotAllowed(['POST'])
        request.session['showEthnicity'] = request.POST.get("showEthnicity", "true") == "true"
        return HttpResponse(True)


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
