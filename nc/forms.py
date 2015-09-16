import datetime

from django import forms
from django.db.models import Q
from selectable.forms import AutoCompleteWidget, AutoCompleteSelectField

from nc import models as stops
from nc.lookups import AgencyLookup


def addNoneOpt(choices):
    opts = list(choices)
    opts.insert(0, (None, "---"))
    return opts


class SearchForm(forms.Form):
    agency = forms.CharField(
        label='Agency Name',
        widget=AutoCompleteWidget(AgencyLookup),
        help_text="ex: Durham Police Department"
    )
    officer = forms.CharField(required=False, help_text="ex: 227")
    start_date = forms.DateField(required=False,
                                 help_text="ex: 8/13/2012")
    end_date = forms.DateField(required=False,
                               help_text="ex: 8/13/2012")
    purpose = forms.MultipleChoiceField(required=False,
                                        choices=stops.PURPOSE_CHOICES,
                                        widget=forms.CheckboxSelectMultiple)
    action = forms.MultipleChoiceField(required=False,
                                       choices=stops.ACTION_CHOICES,
                                       widget=forms.CheckboxSelectMultiple)
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=130)
    race = forms.ChoiceField(
        required=False,
        initial=None,
        choices=addNoneOpt(stops.RACE_CHOICES))
    ethnicity = forms.ChoiceField(
        required=False,
        initial=None,
        choices=addNoneOpt(stops.ETHNICITY_CHOICES))

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date is not None and end_date is not None:

            if start_date > end_date:
                err = "End date must be greater than or equal to start-date"
                self.add_error('end_date', err)

            dt = end_date - start_date
            if dt.days > 366:  # allow for leap-year
                err = "Date-range must be less than or equal to one-year"
                self.add_error('end_date', err)

        return cleaned_data

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
        start_date = self.cleaned_data['start_date']
        if start_date:
            query &= Q(stop__date__gte=start_date)
        end_date = self.cleaned_data['end_date']
        if end_date:
            query &= Q(stop__date__lte=end_date + datetime.timedelta(days=1))
        age = self.cleaned_data['age']
        if age:
            query &= Q(stop__person__age=age) & Q(stop__person__type="D")
        race = self.cleaned_data['race']
        if race:
            query &= Q(stop__person__race=race) & Q(stop__person__type="D")
        ethnicity = self.cleaned_data['ethnicity']
        if ethnicity:
            query &= Q(stop__person__ethnicity=ethnicity) & Q(stop__person__type="D")
        purpose = self.cleaned_data['purpose']
        if purpose:
            query &= Q(stop__purpose__in=purpose)
        action = self.cleaned_data['action']
        if action:
            query &= Q(stop__action__in=action)
        return query


class AgencySearchForm(forms.Form):
    agency = AutoCompleteSelectField(AgencyLookup, required=True)
    agency.widget.attrs['placeholder'] = "Search for police or sheriff's department..."
    agency.widget.attrs['class'] = 'form-control'
    agency.error_messages = {
        "required": """Please select an agency; agency options are available
                       after typing a few characters in the agency name."""
    }
