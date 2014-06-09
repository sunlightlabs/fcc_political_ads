import re

from django.core.management.base import BaseCommand, CommandError
from fccpublicfiles.models import PoliticalBuy
from django.core.paginator import Paginator


invoice_res = [re.compile(r'invoice', re.I)]
invalid_res = [re.compile(r'rebate', re.I), re.compile(r'nab\s+form', re.I), re.compile(r'rebate', re.I), re.compile(r'refund', re.I), re.compile(r'cancel', re.I), re.compile(r'rate card', re.I), re.compile(r'disclosure', re.I)]

class Command(BaseCommand):
    help = "set invoices, etc"
    
    def handle(self, *args, **options):
        chunk_size = 500
        
        buys = PoliticalBuy.objects.exclude(is_invoice=True).exclude(is_FCC_doc=False).select_related('related_FCC_file')
        paginator = Paginator(buys, chunk_size)
        count = 0
        for this_page in paginator.page_range:
            for buy in paginator.page(this_page).object_list:
                for this_re in invoice_res:
                    try:
                        if re.search(this_re, buy.related_FCC_file.raw_url):
                            count += 1
                            buy.is_invoice=True
                            buy.save_no_update()
                    except AttributeError:
                        continue
        print "Found %s invoices" % (count)
        
        count = 0
        invalid_count = 0
        
        buys = PoliticalBuy.objects.exclude(is_invalid=True).exclude(is_FCC_doc=False).select_related('related_FCC_file')
        paginator = Paginator(buys, chunk_size)
        for this_page in paginator.page_range:
            for buy in paginator.page(this_page).object_list:
                for this_re in invalid_res:
                    try:
                        if re.search(this_re, buy.related_FCC_file.raw_url):
                            invalid_count += 1
                            buy.is_invalid=True
                            buy.save_no_update()
                    except AttributeError:
                        continue
        print "Found %s invalids" % (invalid_count)