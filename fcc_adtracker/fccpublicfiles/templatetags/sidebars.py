from django import template

from fccpublicfiles.models import PoliticalBuy
from broadcasters.views import MAX_DOCUMENTS_TO_SHOW_IN_SIDEBAR

register = template.Library()

@register.inclusion_tag('recent_documents_sidebar.html')
def recent_buy_sidebar():
    ad_buys = PoliticalBuy.objects.public().order_by('-created_at')[:MAX_DOCUMENTS_TO_SHOW_IN_SIDEBAR]
    return {
    'ad_buys':ad_buys,
    }
