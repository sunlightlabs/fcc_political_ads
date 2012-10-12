import re

from django.core.management.base import BaseCommand, CommandError
from fccpublicfiles.models import PoliticalBuy

invoice_res = [re.compile(r'invoice', re.I)]
invalid_res = [re.compile(r'rebate', re.I), re.compile(r'nab\s+form', re.I), re.compile(r'rebate', re.I), re.compile(r'refund', re.I), re.compile(r'cancel', re.I), re.compile(r'rate card', re.I), re.compile(r'disclosure', re.I)]
nabform_res = [re.compile(r'nab\s+form', re.I)]

class Command(BaseCommand):
    help = "set invoices, etc"
    
    def handle(self, *args, **options):
        count = 0
        buys = PoliticalBuy.objects.exclude(is_invoice=True).exclude(is_FCC_doc=False).select_related('related_FCC_file')
        
        for buy in buys:
            for this_re in invoice_res:
                if re.search(this_re, buy.related_FCC_file.raw_url):
                    count += 1
                    buy.is_invoice=True
                    buy.save_no_update()
                    
        print "Found %s invoices" % (count)
        
        count = 0
        buys = PoliticalBuy.objects.exclude(is_invalid=True).exclude(is_FCC_doc=False).select_related('related_FCC_file')
        
        rebate_count = 0
        for buy in buys:
            for this_re in invoice_res:
                if re.search(this_re, buy.related_FCC_file.raw_url):
                    rebate_count += 1
                    buy.is_invalid=True
                    buy.save_no_update()
                    
        print "Found %s rebates" % (count)
        
        
        nab_count = 0
        for buy in buys:
            for this_re in nabform_res:
                if re.search(this_re, buy.related_FCC_file.raw_url):
                    nab_count += 1
                    buy.is_invalid=True
                    buy.save_no_update()
                    
        print "Found %s nab forms" % (nab_count)