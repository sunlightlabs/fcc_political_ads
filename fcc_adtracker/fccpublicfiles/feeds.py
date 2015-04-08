from django.contrib.syndication.views import Feed, FeedDoesNotExist
from fccpublicfiles.models import PoliticalBuy, dma_summary, state_summary
from django.shortcuts import get_object_or_404
from django.contrib.localflavor.us import us_states
from django.http import Http404

STATES_DICT = dict(us_states.US_STATES)

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
        return PoliticalBuy.objects.filter(dma_id=obj.dma_id, is_FCC_doc=True).order_by('-related_FCC_file__upload_time', '-upload_time')[:30]
        
    def item_pubdate(self, item):
        return item.related_FCC_file.upload_time



class StateFeed(Feed):
    description_template = 'feeds/market_description.html'

    def get_object(self, request, state_abbreviation):        
        return get_object_or_404(state_summary, state_id=state_abbreviation)


    def title(self, obj):
        return "Political Ad Sleuth: Recent ad buy documents reported in %s" % obj.state_id

    def item_title(self, obj):
        return obj.related_FCC_file

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Political Ad Sleuth: Recent ad buy documents reported in %s" % obj.state_id

    def items(self, obj):
        return PoliticalBuy.objects.filter(community_state=obj.state_id, is_FCC_doc=True).order_by('-related_FCC_file__upload_time', '-upload_time')[:30]

    def item_pubdate(self, item):
        return item.related_FCC_file.upload_time