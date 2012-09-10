from django import forms
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse_lazy
from doccloud.models import Document
from fccpublicfiles.models import PoliticalBuy, Organization, Person
from broadcasters.models import Broadcaster


class SelectWithPopUp(forms.Select):
    model = None

    def __init__(self, model=None, add_url=None):
        self.model = model
        self.add_url = add_url
        super(SelectWithPopUp, self).__init__()

    def render(self, name, *args, **kwargs):
        html = super(SelectWithPopUp, self).render(name, *args, **kwargs)

        if not self.model:
            self.model = name

        popupplus = render_to_string("_form_popuplink.html", {'field': name, 'model': self.model, 'add_url': self.add_url})
        return html + popupplus


class DocCloudFormBase(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization


class SimpleOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ('addresses', 'employees', 'is_visible', 'organization_type')


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person


class PoliticalBuyFormBase(forms.ModelForm):
    class Meta:
        model = PoliticalBuy
        fields = ('broadcasters',)


class PrelimDocumentForm(DocCloudFormBase, PoliticalBuyFormBase):
    broadcasters = forms.ModelMultipleChoiceField(queryset=Broadcaster.objects.all())


class PoliticalBuyFormFull(forms.ModelForm):
    class Meta:
        model = PoliticalBuy
        fields = (
            'advertiser',
            'total_spent_raw',
            'num_spots_raw',
            'contract_start_date',
            'contract_end_date',
            'contract_number',
            'advertiser_signatory',
            'bought_by',
            'lowest_unit_price',
            'is_complete',
            'broadcasters',
        )

    advertiser = forms.ModelChoiceField(queryset=Organization.objects.filter(organization_type='AD'),
                                        widget=SelectWithPopUp(add_url=reverse_lazy('add_advertiser'))
                                        )
    bought_by = forms.ModelChoiceField(queryset=Organization.objects.filter(organization_type='MB'),
                                        widget=SelectWithPopUp(add_url=reverse_lazy('add_media_buyer'))
                                        )

    def __init__(self, *args, **kwargs):
        super(PoliticalBuyFormFull, self).__init__(*args, **kwargs)
        for fieldname in 'advertiser advertiser_signatory bought_by broadcasters'.split():
            append_ajax_class(self.fields[fieldname])


def append_ajax_class(field):
    if field.widget.attrs.has_key('class'):
        field.widget.attrs['class'] += ' suggestions'
    else:
        field.widget.attrs.update({'class':'suggestions'})
