import urllib2, json

from time import sleep
from dateutil.parser import parse as dateparse


from django.core.management.base import BaseCommand, CommandError

from scraper.utils import read_url
from scraper.models import StationData


def get_data_about_callsign(callsign):
    """ Hit the FCC api to fill in details about a station. """
    # sometimes callsigns include -TV... 
    
    json_api = "https://data.fcc.gov/mediabureau/v01/tv/facility/search/%s.json" % callsign
    try:
        response = read_url(json_api)
    except urllib2.HTTPError:
        print "No data for callsign %s. The FCC API could be down." % (callsign)
        return None 
    
    response_read = json.loads(response)
    station_list = None
    try:
        station_list = response_read['results']['searchList'][0]['facilityList']
        if len(station_list) > 1:
            print "Multiple stations found for callsign=%s" % (callsign)
            return None
            
    except IndexError:
        print "Couldn't find any information about %s from the FCC's api" % (callsign)
        return None
    
    try:
        return station_list[0]
    except IndexError:
        print "Empty station list %s" % (callsign)

class Command(BaseCommand):
    
    requires_model_validation = False
    
    def handle(self, *args, **options):
        all_stations = StationData.objects.all()
        print "handling %s stations" % len(all_stations)
        
        
        for count, station in enumerate(all_stations):
            
            api_data = get_data_about_callsign(station.callSign)
            
            if api_data:
                try:
                        
                    station.networkAfil = api_data['networkAfil']
                    station.facilityType = api_data['facilityType']
                    station.service = api_data['service']
                    station.frequency = api_data['frequency']
                    station.band = api_data['band']
                    station.virtualChannel = api_data['virtualChannel']
                    station.rfChannel = api_data['rfChannel']
                    station.communityCity = api_data['communityCity']
                    station.communityState = api_data['communityState']
                    station.nielsenDma = api_data['nielsenDma']
                    station.status = api_data['status']
                    station.partyName = api_data['partyName']
                    station.partyAddress1 = api_data['partyAddress1']
                    station.partyAddress2 = api_data['partyAddress2']
                    station.partyCity = api_data['partyCity']
                    station.partyState = api_data['partyState']
                    station.partyZip1 = api_data['partyZip1']
                    station.partyZip2 = api_data['partyZip2']
                    station.partyPhone = api_data['partyPhone']
                
                    if api_data['statusDate']:
                        station.statusDate = dateparse(api_data['statusDate'])
            
                    if api_data['licenseExpirationDate']:
                        station.licenseExpirationDate = dateparse(api_data['licenseExpirationDate'])
                
                
                    station.save()
                except KeyError:
                    print "KeyError %s" % (station.callSign)
                
            if count % 100 == 0:
                print "processed %s stations" % count
            sleep(0.1)
        