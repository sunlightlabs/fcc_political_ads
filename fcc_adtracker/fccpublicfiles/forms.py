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
        exclude = ('is_visible',)

    def __init__(self, *args, **kwargs):
        super(PoliticalBuyFormFull, self).__init__(*args, **kwargs)
        self.fields['total_spent_raw'].label = 'Grand Total'
        for fieldname in 'advertiser advertiser_signatory bought_by broadcasters'.split():
            append_ajax_class(self.fields[fieldname])


def append_ajax_class(field):
    if field.widget.attrs.has_key('class'):
        field.widget.attrs['class'] += ' suggestions'
    else:
        field.widget.attrs.update({'class':'suggestions'})
