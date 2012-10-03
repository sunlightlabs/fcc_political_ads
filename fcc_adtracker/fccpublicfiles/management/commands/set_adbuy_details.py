# Need to attach advertiser type to ad buy.

from django.core.management.base import BaseCommand, CommandError

from fccpublicfiles.models import PoliticalBuy

class Command(BaseCommand):
    help = "One off to set PDF_File data in ad buys"
    requires_model_validation = False
    
    def handle(self, *args, **options):
        fcc_docs = PoliticalBuy.objects.filter(is_FCC_doc=True)
        for doc in fcc_docs:
            related_pdf = doc.related_FCC_file
            doc.nielsen_dma = related_pdf.nielsen_dma
            doc.dma_id = related_pdf.dma_id
            doc.community_state = related_pdf.community_state
            doc.candidate_type = related_pdf.candidate_type()
            doc.upload_time = related_pdf.upload_time
            doc.save(None)
            print "***setting dma:%s state %s candiddate %s " % (related_pdf.dma_id, related_pdf.community_state, related_pdf.candidate_type())