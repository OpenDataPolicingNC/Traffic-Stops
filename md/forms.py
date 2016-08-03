from django import forms
from selectable.forms import AutoCompleteSelectField

from md.lookups import AgencyLookup


class AgencySearchForm(forms.Form):
    agency = AutoCompleteSelectField(AgencyLookup, required=True)
    agency.widget.attrs['placeholder'] = "Search for police or sheriff's department..."
    agency.widget.attrs['class'] = 'form-control'
    agency.error_messages = {
        "required": """Please select an agency; agency options are available
                       after typing a few characters in the agency name."""
    }
