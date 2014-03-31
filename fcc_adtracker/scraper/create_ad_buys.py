# Create an ad buy from an FCC pdf file. Simplified enormously by not uploading PDF's and doing the document cloud dance.

from fccpublicfiles.models import PoliticalBuy
from scraper.models import PDF_File
from broadcasters.models import Broadcaster
from django.contrib.auth.models import User


def make_ad_buy_from_pdf_file(pdf_file_pk):
    pdf_file = None
    try:
        pdf_file = PDF_File.objects.get(pk=pdf_file_pk)
    except PDF_File.DoesNotExist:
        return None

    auser = User.objects.all()[0]

    pol_buy = PoliticalBuy()
    pol_buy.is_FCC_doc= True
    pol_buy.related_FCC_file = pdf_file
    
    pol_buy.candidate_type = pdf_file.candidate_type()
    pol_buy.fcc_folder_name = pdf_file.raw_name_guess
    pol_buy.nielsen_dma = pdf_file.nielsen_dma
    pol_buy.dma_id = pdf_file.dma_id
    pol_buy.community_state =pdf_file.community_state
    pol_buy.upload_time = pdf_file.upload_time
    pol_buy.contract_start_date = pdf_file.upload_time
    pol_buy.contract_end_date = pdf_file.upload_time
    pol_buy.advertiser_display_name = pdf_file.raw_name_guess or "" + "-" + pdf_file.file_name()
    pol_buy.broadcaster_callsign = pdf_file.callsign
    pol_buy.in_document_cloud = pdf_file.in_document_cloud
    
    pol_buy.save(auser)

    if pdf_file.facility_id:
        try:
            thisbroadcaster = Broadcaster.objects.get(facility_id=pdf_file.facility_id)
            pol_buy.broadcasters.add(thisbroadcaster)
            pol_buy.is_public=True
            pol_buy.save(auser)
        except Broadcaster.DoesNotExist:
            pass
        except Broadcaster.MultipleObjectsReturned:
            pass
                
        return True