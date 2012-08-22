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
