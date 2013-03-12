from django.contrib.syndication.views import Feed, FeedDoesNotExist
from fccpublicfiles.models import PoliticalBuy, dma_summary
from django.shortcuts import get_object_or_404

class MarketFeed(Feed):
    description_template = 'feeds/market_description.html'

    def get_object(self, request, dma_id):
        return get_object_or_404(dma_summary, dma_id=dma_id)

    def title(self, obj):
        return "Political Ad Sleuth: Recent ad buy documents reported in %s" % obj.dma_name
        
    def item_title(self, obj):
        return obj.related_FCC_file
        
    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Political Ad Sleuth: Recent ad buy documents reported in %s" % obj.dma_name

    def items(self, obj):
        return PoliticalBuy.objects.filter(dma_id=obj.dma_id, is_FCC_doc=True).order_by('-upload_time')[:30]