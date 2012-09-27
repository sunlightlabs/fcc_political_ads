# Create an ad buy from an FCC pdf file. Simplified enormously by not uploading PDF's and doing the document cloud dance.



from fccpublicfiles.models import PoliticalBuy
from scraper.models import PDF_File
from django.contrib.auth.models import User


def make_ad_buy_from_pdf_file(pdf_file):
    
    try:
        PoliticalBuy.objects.get(related_FCC_file__pk=pdf_file.pk)
        print "Found buy"
        return False
        
    except PoliticalBuy.DoesNotExist:

        auser = User.objects.all()[0]

        pol_buy = PoliticalBuy()
        pol_buy.is_FCC_doc= True
        pol_buy.related_FCC_file = pdf_file
        pol_buy.save(auser)
    
        if pdf_file.folder.broadcaster:
            pol_buy.broadcasters.add(pdf_file.folder.broadcaster)
            pol_buy.is_public=True
            pol_buy.save(auser)
        
        return True