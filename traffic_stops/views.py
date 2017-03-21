from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic import View, TemplateView

from tsdata.dataset_facts import get_dataset_facts_context


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['navbar_inverse'] = True
        context.update(get_dataset_facts_context())
        return context


class About(TemplateView):
    template_name = "about.html"


class UpdateSession(View):

    http_method_names = (u'post', )

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseNotAllowed(['POST'])
        request.session['showEthnicity'] = request.POST.get("showEthnicity", "true") == "true"
        return HttpResponse(True)
