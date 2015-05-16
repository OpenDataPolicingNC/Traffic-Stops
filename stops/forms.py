import datetime

from django import forms
from django.db.models import Q
from selectable.forms import AutoCompleteWidget, AutoCompleteSelectField

from stops import models as stops
from stops.lookups import AgencyLookup


class SearchForm(forms.Form):
    agency = forms.CharField(
        label='Agency Name',
        widget=AutoCompleteWidget(AgencyLookup),
        help_text="ex: Durham Police Department"
    )
    officer = forms.CharField(required=False, help_text="ex: 227")
    date = forms.DateField(help_text="ex: 8/13/2012")
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
            query &= Q(stop__agency=agency)
        officer = self.cleaned_data['officer']
        if officer:
            query &= Q(stop__officer_id=officer)
        date = self.cleaned_data['date']
        if date:
            query &= Q(stop__date__gte=date,
                       stop__date__lt=date + datetime.timedelta(days=1))
        purpose = self.cleaned_data['purpose']
        if purpose:
            query &= Q(stop__purpose__in=purpose)
        action = self.cleaned_data['action']
        if action:
            query &= Q(stop__action__in=action)
        return query


class AgencySearchForm(forms.Form):
    agency = AutoCompleteSelectField(AgencyLookup, required=False)
    agency.widget.attrs['placeholder'] = "Search for police or sheriff's department..."
    agency.widget.attrs['class'] = 'form-control'
