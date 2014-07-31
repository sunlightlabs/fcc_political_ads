import csv, re

from dateutil.parser import parse as dateparse
from optparse import make_option


from django.core.management.base import BaseCommand, CommandError
from scraper.fcc_scraper import parse_file_url
from scraper.create_ad_buys import make_ad_buy_from_pdf_file

from scraper.models import PDF_File
from broadcasters.models import Broadcaster
from django.contrib.auth.models import User
from fccpublicfiles.models import PoliticalBuy

fcc_infile_identifier = re.compile(r'\((\d{14})\)')



# dict mapping field names. Could go elsewhere, but... 
default_options = {
#    'contract_number': 'order_revision',
    'contract_number':'contract_number',
    'advertiser_name_exact': 'advertiser_name',
    'ad_buyer_exact': 'agency_name',
    'contract_start_date':'flight_date_start',
    'contract_end_date':'flight_date_end',
    'total_spent_raw':'gross_amount',
    'num_spots_raw':'number_of_spots',
    'raw_url':'file_url',
    'upload_time':'upload_time',
    'file_size':'file_size',
}


auser = User.objects.all()[0]

def clean_numeric(string_data):
    string_data = string_data.replace("$","")
    string_data = string_data.replace(",","")
    return float(string_data)
    

def enter_pdf_file(thisfile):
    upload_time = None
    try:
        timefound = thisfile['datefound']
        timefound = timefound.replace('Today at', todays_date)
        upload_time = dateparse(timefound)
    except:
        pass

    if thisfile['raw_url']:
        (facility_id, details) = parse_file_url(thisfile['raw_url'])
        is_outside_group = True
        office = None
        district = None
        if (details[1] == 'Non-Candidate Issue Ads'):
            is_outside_group = True 
        elif (details[1] == 'Federal'):
            office = details[2]
            if (office == 'US House'):
                district = details[3]
        # They're not very consisten about this... 
        path = details[1:]
        name = path[-2:-1][0]

        # hard truncate. This data's a mess.
        federal_office = None
        federal_district = None
    
        ad_type =details[1]
        if office:
            federal_office = office[:31]
        if district:
            federal_district = district[:31]
        raw_name_guess = name[:255]
    
        nielsen_dma = None
        callsign = None
        nielsen_dma = None
        community_state = None
        dma_id = None
    
        try:
            thisbroadcaster = Broadcaster.objects.get(facility_id=facility_id)
            callsign = thisbroadcaster.callsign
            nielsen_dma = thisbroadcaster.nielsen_dma
            community_state = thisbroadcaster.community_state
            dma_id = thisbroadcaster.dma_id
        except Broadcaster.DoesNotExist:
            pass
        
        (pdffile, created) = PDF_File.objects.get_or_create(raw_url=thisfile['raw_url'],   defaults={'size':thisfile['file_size'],'upload_time':upload_time,'ad_type':ad_type, 'federal_office':federal_office, 'federal_district':federal_district, 'facility_id':facility_id, 'callsign':callsign, 'nielsen_dma':nielsen_dma, 'dma_id':dma_id, 'community_state':community_state, 'raw_name_guess':raw_name_guess})
        # make an ad buy object from it as well. 
        if created:
            return pdffile
        else: 
            return None
    
    else:
        message = "couldn't parse pdf file %s" % thisfile
        print message
        return None


def get_fcc_id(stringtext):
    if not stringtext:
        return None
    this_id = None
    idfound = re.search(fcc_infile_identifier, stringtext)
    if idfound:
        this_id = idfound.group(1)
        #print "Got id  %s from %s" % (this_id, stringtext)
    else:
        print "Missing id in %s" % stringtext
    return this_id
            
def handle_row_data(this_data, create_new_ads):
    #print this_data
    # does it exist as a pdf file? 
    pdffile = None
    adbuy = None
    fcc_id = get_fcc_id(this_data['raw_url'])
    if fcc_id:
        try:
            pdffile = PDF_File.objects.get(alternate_id=fcc_id)
        except PDF_File.DoesNotExist:
        
            if create_new_ads:
                print "Missing file %s -- now creating" % (this_data['raw_url'])
            
                pdffile = enter_pdf_file(this_data)
                if pdffile:
                    adbuy = make_ad_buy_from_pdf_file(pdffile.pk)
            else:
                print "Missing file %s -- skipping" % (this_data['raw_url'])
            
            
        # if we don't have the related ad buy, get it. 
        if pdffile:
            try:
                adbuy = PoliticalBuy.objects.get(related_FCC_file=pdffile)
            except PoliticalBuy.DoesNotExist:
                # This shouldn't really happen...
                print "No PoliticalBuy found for ad buy %s" % (pdffile)
                return None
    
            if this_data['total_spent_raw']:
                this_data['total_spent_raw'] = clean_numeric(this_data['total_spent_raw'])
    
            for key in this_data.keys():
                try:
                    current_value = getattr(adbuy, key)
                except AttributeError:
                    continue
                if not current_value:
                    if this_data[key]:
                        setattr(adbuy, key, this_data[key]) 
                        print "Setting %s %s in %s" % (key, this_data[key], adbuy)
            adbuy.save(auser)
        
    return None
    



class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option('--create',
                action='store_true',
                dest='create',
                default=False,
                help='Create new ad documents if they are not found'),
            ) + (
                make_option('--extra_rows',
                action='store',
                dest='extra_rows',
                default=0,
                help='Ignore first n lines'),
            ) + (
                make_option('--excel',
                action='store_true',
                dest='excel',
                default=False,
                help='Use excel-dialect csv'),
                )
    # todo -- allow alternate csv header names to be set from a file specified by the command line--i.e. --bindings=/some/path.py
    
    requires_model_validation = False
    
    help = ('Sets ad data from a csv file. Must specify the file name.')
    args = '[file name]'
    
    def handle(self, *args, **options):
        if not args:
            raise CommandError('Invalid arguments, must provide: %s' % self.args)
        
        filename = args[0]
        print "Processing file '%s' " % (filename)
        
        infile = open(filename, 'r')
        
        create_new_ads = options['create']
        if create_new_ads:
            print "Will create new ads when applicable"
        
        
        extra_rows = int(options['extra_rows'])
        if extra_rows:
            print "Disregarding first %s rows from csv file" % (extra_rows) 
            # Skip the first n lines before looking for headers, if requested.
            for i in range(0,extra_rows):
                next(infile)
        
        reader = None
        excel = options['excel']
        if excel:
            print "Trying to parse csv using excel dialect"
            reader = csv.DictReader(infile, dialect='excel')
        else:
            reader = csv.DictReader(infile)
            
        
        for row in reader:
            this_row_data = {}
            for key in default_options.keys():
                try:
                    this_row_data[key] = row[default_options[key]]
                except KeyError:
                    this_row_data[key] = None
            
            # get date objects for the dates entered. Assumes the dates don't need additional transformation.
            if this_row_data['contract_start_date']:
                this_row_data['contract_start_date'] = dateparse(this_row_data['contract_start_date'])
            if this_row_data['contract_end_date']:
                this_row_data['contract_end_date'] = dateparse(this_row_data['contract_end_date'])
            if this_row_data['upload_time']:
                this_row_data['upload_time'] = dateparse(this_row_data['upload_time']).date()
            
            
            
            #print this_row_data
            
            handle_row_data(this_row_data, create_new_ads)
            
        
        
        