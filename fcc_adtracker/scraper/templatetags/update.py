from django.template import Library
from scraper.models import Scrape_Time

register = Library()


@register.inclusion_tag('_update_time.html')  
def updatetime():
    most_recent_scrape=Scrape_Time.objects.all().order_by('-run_time')[0]
    return {
    'most_recent_scrape':most_recent_scrape,
    }
