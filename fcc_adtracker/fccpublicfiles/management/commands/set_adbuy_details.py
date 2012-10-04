# Need to attach advertiser type to ad buy.

from django.core.management.base import BaseCommand, CommandError

from fccpublicfiles.models import PoliticalBuy

class Command(BaseCommand):
    help = "One off to set PDF_File data in ad buys"
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        nonfcc_docs = PoliticalBuy.objects.filter(is_FCC_doc=False)
        for doc in nonfcc_docs:
            doc.upload_time = doc.contract_end_date
            doc.save(None)
            
        fcc_docs = PoliticalBuy.objects.filter(is_FCC_doc=True)
        for doc in fcc_docs:
            related_pdf = doc.related_FCC_file
            doc.nielsen_dma = related_pdf.nielsen_dma
            doc.dma_id = related_pdf.dma_id
            doc.community_state = related_pdf.community_state
            doc.candidate_type = related_pdf.candidate_type()
            doc.upload_time = related_pdf.upload_time
            doc.advertiser_display_name = related_pdf.raw_name_guess + "-" + related_pdf.file_name()
            doc.broadcaster_callsign = related_pdf.folder.broadcaster.callsign
            doc.ignore_post_save = True
            doc.save(None)
            print "***setting dma:%s state %s candiddate %s callsign %s" % (related_pdf.dma_id, related_pdf.community_state, related_pdf.candidate_type(), doc.broadcaster_callsign )
            
            
         