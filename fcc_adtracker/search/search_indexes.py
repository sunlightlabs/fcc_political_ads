from haystack import indexes

from fccpublicfiles.models import PoliticalBuy

# Search elasticsearch index: http://127.0.0.1:9200/pas/modelresult/_search
# http://127.0.0.1:9200/pas/modelresult/_search?q=text:American%20Action


class PoliticalBuyIndex(indexes.SearchIndex, indexes.Indexable):
    """Index of PUBLIC PolticalBuys"""
    text = indexes.CharField(document=True, use_template=True)
    relatedfccfile = indexes.CharField(model_attr='related_FCC_file', null=True, default='', faceted=False)
    advertiser = indexes.CharField(model_attr='advertiser', null=True, default='Unknown', faceted=True)
#    advertiser_signatory = indexes.CharField(model_attr='advertiser_signatory', null=True, default='Unknown', faceted=True)
#    media_buyer = indexes.CharField(model_attr='bought_by', null=True, default='Unknown', faceted=False)
    state = indexes.MultiValueField(faceted=True)
    station = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return PoliticalBuy

    def get_updated_field(self):
        return 'updated_at'

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_station(self, obj):
        return obj.broadcasters_callsign_list()
    
    def prepare_state(self, obj):
        return obj.broadcasters_state_list()
