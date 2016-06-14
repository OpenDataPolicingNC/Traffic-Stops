from django.shortcuts import render


def home(request):
    # if request.method == 'GET' and request.GET:
    #     form = forms.AgencySearchForm(request.GET)
    #     if form.is_valid():
    #         agency = form.cleaned_data['agency']
    #         return redirect('agency-detail', agency.pk)
    # else:
    #     form = forms.AgencySearchForm()
    # context = {'agency_form': form}
    return render(request, 'md.html') #, context)
