from django import forms
from django.db.models import Q
from selectable.forms import AutoCompleteWidget

from stops import models as stops
from stops.lookups import AgencyLookup


class SearchForm(forms.Form):
    agency = forms.CharField(
        label='Agency Name',
        widget=AutoCompleteWidget(AgencyLookup),
        required=False,
    )
    driver_arrest = forms.BooleanField(required=False)
    passenger_arrest = forms.BooleanField(required=False)
    encounter_force = forms.BooleanField(required=False)
    engage_force = forms.BooleanField(required=False)
    officer_injury = forms.BooleanField(required=False)
    driver_injury = forms.BooleanField(required=False)
    passenger_injury = forms.BooleanField(required=False)
    purpose = forms.MultipleChoiceField(required=False,
                                        choices=stops.PURPOSE_CHOICES,
                                        widget=forms.CheckboxSelectMultiple)
    action = forms.MultipleChoiceField(required=False,
                                       choices=stops.ACTION_CHOICES,
                                       widget=forms.CheckboxSelectMultiple)

    def clean_agency(self):
        agency = self.cleaned_data['agency']
        if agency:
            try:
                agency = stops.Agency.objects.get(name=agency)
            except stops.Agency.DoesNotExist:
                agency = None
        return agency

    def get_query(self):
        query = Q()
        agency = self.cleaned_data['agency']
        if agency:
            query &= Q(agency=agency)
        purpose = self.cleaned_data['purpose']
        if purpose:
            query &= Q(purpose__in=purpose)
        driver_arrest = self.cleaned_data['driver_arrest']
        if driver_arrest:
            query &= Q(driver_arrest=True)
        action = self.cleaned_data['action']
        if action:
            query &= Q(action__in=action)
        return query
