from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteSelectField
from django.forms import ModelForm, ModelMultipleChoiceField
from doccloud.models import Document
from fccpublicfiles.models import PoliticalBuy
from broadcasters.models import Broadcaster


class DocCloudFormBase(ModelForm):
    class Meta:
        model = Document
        fields = ('file',)


class PoliticalBuyFormBase(ModelForm):
    class Meta:
        model = PoliticalBuy
        fields = ('broadcasters',)


class PrelimDocumentForm(DocCloudFormBase, PoliticalBuyFormBase):
    broadcasters = ModelMultipleChoiceField(queryset=Broadcaster.objects.all())


class PoliticalBuyFormFull(ModelForm):
    class Meta:
        model = PoliticalBuy

    def __init__(self, *args, **kwargs):
        super(PoliticalBuyFormFull, self).__init__(*args, **kwargs)
        self.fields['total_spent_raw'].label = 'Grand Total'
        self.fields['advertiser'] = AutoCompleteSelectField('organization', required=False)
        self.fields['advertiser_signatory'] = AutoCompleteSelectField('person', required=False)
        self.fields['bought_by'] = AutoCompleteSelectField('organization', required=False)
        self.fields['broadcasters'] = AutoCompleteSelectMultipleField('broadcaster', required=False)
