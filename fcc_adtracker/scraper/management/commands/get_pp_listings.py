import urllib2
import csv
import re

from django.core.management.base import BaseCommand, CommandError
from dateutil.parser import parse as dateparse
from time import sleep

from scraper.models import ftf_reference


#def process_pp_csv(url):


url_re = r'"(http://projects.propublica.org/free-the-files/filings/\d+)"'
fcc_identifier = re.compile(r'\((\d{14})\)')

class Command(BaseCommand):
    help = "Read Propublica's data files and add newly freed files to db, so we can cite data"
    
    requires_model_validation = False
    
    def handle(self, *args, **options):
        
        market_list = ['new-york', 'philadelphia', 'boston-manchester', 'washington-dc-hagrstwn', 'atlanta', 'detroit', 'phoenix-prescott', 'tampa-st-pete-sarasota', 'minneapolis-st-paul', 'miami-ft-lauderdale', 'denver', 'cleveland-akron-canton', 'orlando-daytona-bch-melbrn', 'st-louis', 'pittsburgh', 'raleigh-durham-fayetvlle', 'charlotte', 'hartford-new-haven', 'kansas-city', 'columbus-oh', 'salt-lake-city', 'milwaukee', 'cincinnati', 'greenvll-spart-ashevll-and', 'west-palm-beach-ft-pierce', 'las-vegas', 'harrisburg-lncstr-leb-york', 'grand-rapids-kalmzoo-b-crk', 'norfolk-portsmth-newpt-nws', 'albuquerque-santa-fe', 'greensboro-h-point-w-salem', 'memphis', 'jacksonville']
        
        #market_list = ['new-york']
        
        for market_slug in market_list:
            #print "Processing %s" % market_slug
            market_url = "https://projects.propublica.org/free-the-files/filings/select.csv?market=" + market_slug
            print "Getting url: %s" % (market_url)
            market_file = urllib2.urlopen(market_url)
            
            #print market_file
            #dumpfilename = "market_test.csv"
            #outfile = open(dumpfilename, 'w')
            #outfile.write(market_file)
            
            #market_file = open(dumpfilename, 'r')
            reader = csv.reader(market_file)
            header = reader.next()
            count=0
            print "header: %s" % (header)
            for row in reader:
                
                count+= 1
                status = row[0]
                link = ""
                linkfound = re.search(url_re, row[1])
                if linkfound:
                    link = linkfound.group(1)
                callsign = row[2]
                market = row[3]
                v_committee = row[4]
                raw_amt = row[5]
                v_amt = None
                try:
                    v_amt = int(float(raw_amt))
                except:
                    #print "couldn't convert to int: %s" % (raw_amt)
                    pass
                    
                #if status=='Freed File':    
                #print "v_amt = %s in row %s" % (v_amt, row)
                v_agncy = row[6]
                v_contract_no = row[7]
                pp_scrape_date_raw = row[8]
                pp_scrape_date = None
                try:
                    pp_scrape_date = dateparse(pp_scrape_date_raw)
                except:
                    print "couldn't parse scrape date %s" % (pp_scrape_date_raw)
                fcc_upload_date_raw = row[9]    
                fcc_upload_date = None
                try:
                    fcc_upload_date = dateparse(fcc_upload_date_raw)
                except:
                    pass
                    #print "couldn't parse upload date %s" % (fcc_upload_date_raw)
                # they glom metadata into the next few rows
                metadata = ""
                cellnum = 10
                while cellnum < len(row):
                    metadata += "/" + row[cellnum]
                    cellnum += 1
                #print "metadata is %s" % (metadata)
                
                doc_id = None
                fcc_id = re.search(fcc_identifier, metadata)
                if fcc_id:
                    #print "Found id  '%s' in '%s' " % (fcc_id.group(1), metadata)
                    doc_id = fcc_id.group(1)
                else:
                    pass
                    #print "*** no match in %s" % (metadata)
                
                (ftf_ref, created) = ftf_reference.objects.get_or_create(link=link, 
                    defaults={
                        'status':status,
                        'callsign':callsign,
                        'market':market,
                        'v_committee':v_committee,
                        'v_agncy':v_agncy,
                        'v_contract_no':v_contract_no,
                        'v_amt':v_amt,
                        'pp_scrape_date':pp_scrape_date,
                        'fcc_upload_date':fcc_upload_date,
                        'fcc_metadata':metadata,
                        'file_url':link,
                        'doc_id':doc_id,
                    })
                # update if it's not new    
                if not created:
                    
                    if status=='Freed File' and ftf_ref.status != 'Freed File':
                        ftf_ref.status = status
                        ftf_ref.v_amt=v_amt
                        ftf_ref.v_contract_no=v_contract_no
                        ftf_ref.v_committee = v_committee
                        ftf_ref.v_agncy = v_agncy
                        ftf_ref.save()
                        
                    elif status=='Not an ad buy' and ftf_ref.status != 'Not an ad buy':
                        ftf_ref.status = status
                        ftf_ref.save()
                    
                    
                #print status, link, callsign, market, v_committee, v_agncy, v_contract_no
            print "Read %s lines. Pausing 3 seconds." % count
            sleep(3)