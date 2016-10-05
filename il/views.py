from . import forms

from traffic_stops import base_views

class Home(base_views.Home):
    form_class = forms.AgencySearchForm
    template_name = 'il.html'
    # success_url = 'il:agency-detail'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        # context['find_a_stop_form'] = forms.SearchForm()
        return context
