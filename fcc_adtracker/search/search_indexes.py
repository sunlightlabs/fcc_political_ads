from haystack import indexes

from fccpublicfiles.models import PoliticalBuy

# Search elasticsearch index: http://127.0.0.1:9200/pas/modelresult/_search
# http://127.0.0.1:9200/pas/modelresult/_search?q=text:American%20Action


class PoliticalBuyIndex(indexes.SearchIndex, indexes.Indexable):
    """Index of PUBLIC PolticalBuys"""
    text = indexes.CharField(document=True, use_template=True)
    type = indexes.CharField(faceted=True, default='')
    relatedfccfile = indexes.CharField(model_attr='related_FCC_file', null=True, default='', faceted=False)
    advertiser = indexes.CharField(model_attr='advertiser', null=True, default='Unknown', faceted=True)
    start_date = indexes.DateField(model_attr='contract_start_date')
    end_date = indexes.DateField(model_attr='contract_end_date')
#    advertiser_signatory = indexes.CharField(model_attr='advertiser_signatory', null=True, default='Unknown', faceted=True)
#    media_buyer = indexes.CharField(model_attr='bought_by', null=True, default='Unknown', faceted=False)
    state = indexes.MultiValueField(faceted=True)
    # station = indexes.MultiValueField(faceted=True)
    source = indexes.CharField(faceted=True, default='')
    status = indexes.CharField(faceted=True, default='')

    def get_model(self):
        return PoliticalBuy

    def get_updated_field(self):
        return 'updated_at'

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_type(self, obj):
        if obj.is_FCC_doc:
            return obj.related_FCC_file.candidate_type()
        else:
            return 'Unknown'

    def prepare_source(self, obj):
        return obj.doc_source()

#    def prepare_station(self, obj):
#        return obj.broadcasters_callsign_list()

    def prepare_state(self, obj):
        return obj.broadcasters_state_list()

    def prepare_status(self, obj):
        #print "Preparing status: %s - status is '%s'" % (obj, obj.doc_status())
        return obj.doc_status()
