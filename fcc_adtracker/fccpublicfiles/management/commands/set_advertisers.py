import re

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from fccpublicfiles.models import PoliticalBuy
from scraper.advertiser_matching.ad_matcher import ad_matcher


urlstart_re = re.compile(r'https://stations.fcc.gov/collect/files/\d+/Political File/2012/.*?\/')
convert_to_whitespace = re.compile('[\s\t_]')

def cleanupstring(raw_alias):
    raw_alias = raw_alias.upper()
    raw_alias = re.sub(convert_to_whitespace, " ", raw_alias)
    raw_alias = re.sub(r'\\', " ", raw_alias)
    raw_alias = re.sub(r'\/', " ", raw_alias)
    raw_alias = raw_alias.strip("'")
    raw_alias = raw_alias.strip('" \'')
    raw_alias = raw_alias.strip("")
    return raw_alias

def cleanupurl(url):
    url_end = re.sub(urlstart_re, "", url)
    return url_end


class Command(BaseCommand):
    help = "Assign advertisers to Political Buys"
    
    def handle(self, *args, **options):
        count = 0
        buys = PoliticalBuy.objects.filter(advertiser__isnull=True).select_related('related_FCC_file')
        
        am = ad_matcher()
#        assert False
        for this_buy in buys:
            url = ""
            try:
                url = this_buy.related_FCC_file.raw_url

            except AttributeError:
                continue
            url = cleanupurl(url)
            url = cleanupstring(url)
            matched_organization = am.match_name(url, this_buy.candidate_type)
            if (matched_organization):
                #pass
                print "Found match for %s" % (url)
                this_buy.advertiser = matched_organization
                this_buy.advertiser_display_name = matched_organization.name
                updated_by = this_buy.updated_by
                # Don't call document cloud
                this_buy.ignore_post_save=True
                this_buy.save(updated_by)
                count += 1
            else:     
                pass
        print "Total matches = %s" % (count)
            