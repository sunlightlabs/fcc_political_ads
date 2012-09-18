from django import forms
from django.forms.extras.widgets import SelectDateWidget

from haystack.forms import FacetedSearchForm

from fccpublicfiles.forms import SELECT_YEARS


class DateRangeSearchForm(FacetedSearchForm):
    start_date = forms.DateField(widget=SelectDateWidget(years=SELECT_YEARS, attrs={'class': 'input-mini'}), required=False)
    end_date = forms.DateField(widget=SelectDateWidget(years=SELECT_YEARS, attrs={'class': 'input-mini'}), required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DateRangeSearchForm, self).search()

        if len(sqs) > 0:
            # Check to see if a start_date was chosen.
            if self.cleaned_data['start_date']:
                sqs = sqs.filter(contract_start_date__gte=self.cleaned_data['start_date'])

            # Check to see if an end_date was chosen.
            if self.cleaned_data['end_date']:
                sqs = sqs.filter(contract_end_date__lte=self.cleaned_data['end_date'])

        return sqs
