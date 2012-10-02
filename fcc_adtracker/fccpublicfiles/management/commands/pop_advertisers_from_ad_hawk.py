import urllib2
import urllib
import csv

try:
    import json
except ImportError:
    import simplejson as json

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from django.conf import settings


from fecdata.models import Committee
from fccpublicfiles.models import TV_Advertiser

try:
    AD_HAWK_MAPPING_URL = getattr(settings, 'AD_HAWK_MAPPING_URL')
except:
    raise("Couldn't import all needed settings--is local settings set?")

class Command(BaseCommand):
    args = '<cycle>'
    help = "Populate part of the advertiser table from ad hawk's json file"
    requires_model_validation = False
    
    def handle(self, *args, **options):
        print "processing mappings" 
        url = AD_HAWK_MAPPING_URL
        data = urllib2.urlopen(url).read()
        data_read = json.loads(data)
        
        for committee in data_read['committees']:
            print "Processing %s" % committee
            name = committee['name']
            
            (ie_url, ftum_url) = (None, None)
            try:
                ie_url =committee['ie_url'],
            except:
                pass
            try:
                ftum_url = committee['ftum_url']
            except:
                pass
            
            (this_adv, created) = TV_Advertiser.objects.get_or_create(advertiser_name=name, defaults={
                'ad_hawk_url':committee['adhawk_url'], 
                'ftum_url':ftum_url,
                'ie_url':ie_url, 
                })
            fec_id = None
            try:
                fec_id = committee['fec_id']
            except KeyError:
                try:
                    fec_id = committee['fec_ids'][0]
                except:
                    pass
                
            try:
                if fec_id:
                    this_committee = Committee.objects.get(fec_id=fec_id)
                    this_adv.primary_committee = this_committee
                    this_adv.is_in_adhawk = True
                    this_adv.save()
            except Committee.DoesNotExist:
                pass
            
            # The primary committee appears in the list of committees; remove it. 
            for id in committee['fec_ids']:
                try:
                    if id == committee['fec_id']:
                        continue
                except:
                    pass
                try:
                    this_committee = Committee.objects.get(fec_id=id)
                    this_adv.secondary_committees.add(this_committee)
                    #committee_name.add(this_committee)
                    this_adv.save()
                except Committee.DoesNotExist:
                    pass
    
    # fix crossroads
    american_crossroads = TV_Advertiser.objects.get(primary_committee__fec_id='C00487363')
    crossroads_gps = Committee.objects.get(fec_id='C90011719')
    american_crossroads.advertiser_name = "CROSSROADS (AMERICAN CROSSROADS AND CROSSROADS GPS)"
    american_crossroads.secondary_committees.add(crossroads_gps)
    american_crossroads.save()