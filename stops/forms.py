from django import forms
from selectable.forms import AutoCompleteWidget


from stops import models as stops
from stops.lookups import AgencyLookup


class SearchForm(forms.Form):
    agency = forms.CharField(
        label='Agency Name',
        widget=AutoCompleteWidget(AgencyLookup),
        required=False,
    )
