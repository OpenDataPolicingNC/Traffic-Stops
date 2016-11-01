from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic import View, TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['navbar_inverse'] = True
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
