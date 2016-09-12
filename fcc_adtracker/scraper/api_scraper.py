import requests
import json
import re
import datetime
import pytz


API_BASE = "https://publicfiles.fcc.gov/api/manager/file/history.json"

result = None
result_json = None

political_re = re.compile('Political\s+File', re.I)
file_url_re = re.compile(r'Political Files/(.+)')


def parse_file_url(url):

    url_parts = re.match(file_url_re, url)
    pathArray = None
    if url_parts:
        print "Got url_parts %s" % url_parts.group(1)
        pathArray = url_parts.group(1).split('/')
    else: 
        print "Couldn't parse file path %s" % (url)
        
    return pathArray

def set_addon_fields(pdf_json, pdf, folder_path):
    print "\nSet addon fields start "
    pdf['is_political_file'] = True
    print "Found political file url: %s" % (folder_path)
    # Found political file url: Political Files/2016/Federal/President/Hillary Clinton
    details = parse_file_url(folder_path)
    if details:
        office = None
        district = None
        print "got details %s" % (details)
        if (details[1] == 'Non-Candidate Issue Ads'):
            is_outside_group = True 
        elif (details[1] == 'Federal'):
            office = details[2]
            if (office == 'US House'):
                try:
                    district = details[3]
                except IndexError:
                    district = None
        # They're not very consisten about this... 
        try:
            name = details[-1:][0]
        except IndexError:
            name = ""
        print "name %s" % (name)
        # hard truncate. This data's a mess.
        ad_type =details[1]
        pdf['ad_type']=ad_type
        if office:
            pdf['federal_office'] = office[:31]
        else:
            pdf['federal_office']=''
        if district:
            pdf['federal_district'] = district[:31]
        else:
            pdf['federal_district']=''

        pdf['raw_name_guess'] = name[:255]
    else:
        print "Details missing"
        pdf['ad_type']=''
        pdf['federal_office']=''
        pdf['federal_district']=''
        pdf['raw_name_guess']=''


    print "Set addon fields end\n"
    return pdf



def create_pdf_filestub_from_json(pdf_json):
    # get or create here

    folder_path = pdf_json['file_folder_path'] 
    file_name =  pdf_json['file_name']
    if re.search(political_re, folder_path) and pdf_json['source_service_code']=='TV' and pdf_json['history_status']=="new":
        print "making pdf from %s" % pdf_json

        raw_url = ''

        pdf = {
            'callsign': pdf_json['callsign'],
            'facility_id':pdf_json['entity_id'],
            'raw_url':folder_path +"/" + file_name,  ## is raw_url the download url? Hmm. 
            'size':pdf_json['file_size'],
            'upload_time':pdf_json['last_update_ts'], # is this accurate for new files?
            'related_candidate_id':None,
            'community_state':pdf_json['state'],
            'download_url':"https://files.fcc.gov/download/%s"%(pdf_json['file_manager_id']),
            'fcc_file_id':pdf_json['file_id'],
            'file_manager_id':pdf_json['file_manager_id'],
            'file_status':pdf_json['file_status'],
            'history_status':pdf_json['history_status'],
            'folder_id':pdf_json['folder_id']
            }
        pdf = set_addon_fields(pdf_json, pdf, folder_path)
        print "\n---pdf is: %s" % pdf
        return pdf
    else: 
        # not a political file for TV
        return None


def parse_api_feed():
    filestubs = []
    # Set the date to be one hour behind eastern time. 
    # This way we're sure to get filings filed before midnight (assuming hourly scrapes)
    now_minus_an_hour = datetime.datetime.now(pytz.timezone('US/Eastern')) - datetime.timedelta(hours=1)
    today_string = "%s-%02d-%02d" % (now_minus_an_hour.year, now_minus_an_hour.month, now_minus_an_hour.day)
    print("Processing files found for %s" % (today_string))

    payload = {'startDate': today_string}
    result = requests.get(API_BASE, params=payload)

    if result.status_code == 200:
        result_json = result.json()        

        history = result_json['history']

        for hist_found in history:
            fs = create_pdf_filestub_from_json(hist_found)
            filestubs.append(fs)
    else:
        print("API call failed with status %s " % result.status_code)

    return filestubs

