""" Given a url, save a copy locally, then push it to document cloud, and make an ad buy from it. 
Need to set the doccloud kv pairs differently in post_save to make clear that this is machine-entered

Do we need to read the pdf file in chunks? None of the files *should* be that big, but... FWIW, I think we know the expected file size 
from the FCC site... 
"""

import urllib2

from urlparse import urlparse

from django.conf import settings
from django.core.files import File

from scraper.utils import read_url
from fccpublicfiles.models import PoliticalBuy
from scraper.models import PDF_File
from doccloud.models import Document
from django.contrib.auth.models import User

SCRAPER_LOCAL_DOC_DIR = getattr(settings, 'SCRAPER_LOCAL_DOC_DIR')

def make_ad_buy_from_pdf_file(pdf_file):
    
    pdf_url = pdf_file.raw_url
    auser = User.objects.all()[0]
    tempfile_name =  urllib2.unquote(urlparse(pdf_url).path)
    tempfile_name = tempfile_name.lstrip('/')
    tempfile_name_fixed = tempfile_name.replace("/", "%%")
    print "temp name is %s" % (tempfile_name_fixed)
    tempfile_full = SCRAPER_LOCAL_DOC_DIR + "/" + tempfile_name_fixed
    page = read_url(pdf_url)
    print "read the pdf"
    tempfile = open(tempfile_full, "wb")
    tempfile.write(page)
    tempfile.close()
    print "wrote the pdf"
    
    file = open(tempfile_full)
    djangofile = File(file)

    print "creating doc"
    d = Document(title=tempfile_name, description="From the FCC's political files", user=auser, access_level='public')

    d.file.save('new', djangofile)
    print "saved via local"
    d.connect_dc_doc()
    d.save()

    print "save 2"

    pol_buy = PoliticalBuy(documentcloud_doc=d)
    pol_buy.is_FCC_doc= True
    pol_buy.related_FCC_file = pdf_file
    pol_buy.save(auser)
    
    if pdf_file.folder.broadcaster:
        pol_buy.broadcasters.add(pdf_file.folder.broadcaster)
        pol_buy.save(auser)
        
    # 
    # Record that this file has been uploaded. 
    pdf_file.in_document_cloud = True
    pdf_file.save()
    return True