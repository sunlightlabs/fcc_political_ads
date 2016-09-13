

from django.db import models
# from django.contrib.gis.db import models

from broadcasters.models import Broadcaster

from utils import get_folder_path, get_file_path
from django.contrib.localflavor.us import us_states

STATES_DICT = dict(us_states.US_STATES)

# Geo representation of a broadcast area. Requires PostGIS. 
"""
class StationContour(models.Model):
    facility_id = models.CharField(max_length=15, primary_key=True)
    callSign = models.CharField(max_length=15)
    station_polygon = models.PolygonField(null=True, srid=4326) # maybe we want 4269 ? 
    objects = models.GeoManager()

    polylines = models.TextField(null=True, editable=False)
    levels = models.CharField(max_length=511, null=True) # Should never be longer than 360, b/c FCC puts out degree-based readings. 
"""


# whenever we run the scraper add it here. Periodically clear this out...
class Scrape_Time(models.Model):
    run_time = models.DateTimeField(auto_now=True)

# Helper reference class to store data about stations scraped from the FCC.
# In general all of the TV stations with data on 'em are in here; broadcasters is only broadcasters we 'care' about. 

# All of this info is available from the CDBS and elsewhere, but having it flattened is super-convenient--saves the pain of picking 
# which application_id is the current one. Actually not clear where studio addresses come from in the CDBS. 
#TODO: unify load process. 
class StationData(models.Model):
    # DATA FROM API
    facility_id = models.CharField(max_length=15, primary_key=True)
    callSign = models.CharField(max_length=15)
    facilityType = models.CharField(max_length=3)
    service= models.CharField(max_length=31, null=True)
    authAppId= models.CharField(max_length=15, null=True)
    frequency = models.CharField(max_length=15, null=True)
    band= models.CharField(max_length=15)
    virtualChannel = models.CharField(max_length=3)
    rfChannel= models.CharField(max_length=3)
    networkAfil= models.CharField(max_length=100, null=True)
    communityCity= models.CharField(max_length=20)
    communityState= models.CharField(max_length=3)
    nielsenDma= models.CharField(max_length=60)
    # Watch out for status = "LICENSED AND SILENT"
    status = models.CharField(max_length=25)
    statusDate= models.DateField(null=True)
    licenseExpirationDate= models.DateField(null=True)
    partyName= models.CharField(max_length=255, null=True)
    partyAddress1= models.CharField(max_length=127, null=True)
    partyAddress2= models.CharField(max_length=127, null=True)
    partyCity= models.CharField(max_length=127, null=True)
    partyState= models.CharField(max_length=7, null=True)
    partyZip1= models.CharField(max_length=15, null=True)
    partyZip2= models.CharField(max_length=15, null=True)
    partyPhone= models.CharField(max_length=15, null=True)
    # From scraping the site. Where is this in the CDBS? 
    studio_address = models.CharField(max_length=255, null=True)
    studio_state = models.CharField(max_length=7, null=True)
    studio_zip = models.CharField(max_length=15, null=True)
    studio_phone = models.CharField(max_length=15, null=True)
    # From the kml files. Should also have as geography. 
    station_lat =  models.FloatField(null=True)# Antenna location
    station_lng =  models.FloatField(null=True) # Antenna location
    
    #station_point = models.PointField(null=True, srid=4326) # maybe we want 4269 ? 
    #objects = models.GeoManager()

    # Added by consulting crosswalk table
    nielsenDma_id = models.IntegerField(null=True)
    is_mandated_station = models.BooleanField(default=False, help_text="Is this station mandated to report political files?")
    
    # TODO
    # house_districts - m2m
    # senate_districts - m2m

    def __unicode__(self):
        return "%s - %s, %s" % (self.callSign, self.communityCity, self.communityState)




# Where did the doc come from? IE, what group? And how do they want to be credited ? 
# Requires manual entry, etc. 
class doc_source(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, help_text="Group's name")
    project_name = models.CharField(max_length=255, blank=True, null=True, help_text="Project name")
    project_link = models.CharField(max_length=255, blank=True, null=True, help_text="link t project")
    use_html = models.BooleanField(max_length=255, blank=True, default=False, help_text="Should we use the html to link to 'em (if there are images, etc.)")
    raw_html = models.TextField(max_length=255, blank=True, null=True, help_text="raw html of credit line to group collecting this doc.")


# Reference to docs already in DC. We don't know their slugs; gotta match to what we know on the basis of titles. 
class dc_reference(models.Model):
    # from DC
    dc_slug = models.CharField(max_length=255, blank=True, null=True, help_text="Document cloud slug")
    dc_title = models.CharField(max_length=255, blank=True, null=True, help_text="Document cloud title")
    #source_url = models.CharField(max_length=255, blank=True, null=True, help_text="Original source url, when available")
    source = models.ForeignKey('doc_source', null=True)

    def __unicode__(self):
        return self.dc_title
        
class ftf_reference(models.Model):
    # data entered by ProPublica users
    status = models.CharField(max_length=15, blank=True, null=True, help_text="freed?")
    link = models.CharField(max_length=255, blank=True, null=True, help_text="link to PP file")
    callsign = models.CharField(max_length=15, blank=True, null=True, help_text="callsign")
    market = models.CharField(max_length=127, blank=True, null=True, help_text="market")
    v_committee = models.CharField(max_length=255, blank=True, null=True, help_text="verified committee")
    v_amt = models.IntegerField(null=True)
    v_agncy= models.CharField(max_length=255, blank=True, null=True, help_text="verified agency")
    v_contract_no = models.CharField(max_length=31, blank=True, null=True, help_text="freed?")
    pp_scrape_date = models.DateTimeField(null=True)
    fcc_upload_date= models.DateTimeField(null=True)
    fcc_metadata = models.CharField(max_length=511, blank=True, null=True, help_text="concatted from their file")
    file_url= models.CharField(max_length=511, blank=True, null=True, help_text="url from FEC")
    doc_id = models.CharField(max_length=15, null=True, help_text="14-digit FEC identifier")
    
    def __unicode__(self):
        return self.file_url

"""
# Represents the basic info in a folder. Folders have types, parents, and children, but that's 'recoverable' from the URL
class Folder(models.Model):
    callsign = models.CharField(max_length=12,)
    facility_id = models.PositiveIntegerField(blank=True, null=True, unique=True, editable=False, help_text='FCC assigned id')
    broadcaster = models.ForeignKey(Broadcaster, blank=True, null=True)
    raw_url = models.CharField(max_length=511, unique=True) # not url encoded
    size = models.IntegerField(blank=True, null=True) # how many files are in it's children
    scrape_time = models.DateTimeField(blank=True, null=True, auto_now=True, help_text="When was this folder last scraped?")
    folder_class = models.CharField(max_length=63, blank=True, null=True, help_text="the entity class in the html: candidate|office...")
    folder_name = models.CharField(max_length=63, blank=True, null=True, help_text="The last element in the path")
    related_candidate_id = models.CharField(max_length=15, blank=True, null=True, help_text="FEC candidate id if this folder represents a candidate")
    related_pac_id = models.CharField(max_length=15, blank=True, null=True, help_text="FEC committee id if this folder represents a committee")
    
    def path(self):
        return get_folder_path(self.raw_url)
    
    def __unicode__(self):
        return self.raw_url

"""

class PDF_File(models.Model):
    callsign = models.CharField(max_length=12)
    facility_id = models.PositiveIntegerField(blank=True, null=True, unique=True, editable=False, help_text='FCC assigned id')
    #folder = models.ForeignKey(Folder)
    raw_url = models.CharField(max_length=511, unique=True, help_text="the URL this was scraped from") # not url encoded
    #
    underscore_url = models.CharField(max_length=511, null=True, help_text="the URL from the feeds") # not url encoded
    filedir_url = models.CharField(max_length=511, null=True, help_text="the URL from the hierarchy") # not url encoded
    containing_folder_path = models.CharField(max_length=511, null=True, help_text="the URL of the folder") # not url encoded
    quickview_folder_path = models.CharField(max_length=511, null=True, help_text="the URL of the folder") # not url encoded
    document_title = models.CharField(max_length=255, blank=True, null=True, help_text="the one given in the feed, not the document title per se")
    
    file_id = models.CharField(max_length=14, null=True, help_text="id of the file without the underscore.")
    alternate_id = models.CharField(max_length=14, null=True, help_text="id of the underscored version of the file, available through the feed")
    size = models.CharField(max_length=31, blank=True, null=True) # how big is it in text?
    upload_time = models.DateTimeField(blank=True, null=True, auto_now=False, help_text="When was this folder last modified?")
    related_candidate_id = models.CharField(max_length=15, blank=True, null=True, help_text="FEC candidate id if this folder represents a candidate")
    related_pac_id = models.CharField(max_length=15, blank=True, null=True, help_text="FEC committee id if this folder represents a committee")

    ad_type = models.CharField(max_length=31, blank=True, null=True, help_text="Federal, State, Local, Non-candidate")
    federal_office =  models.CharField(max_length=31, blank=True, null=True, help_text="President, House, Senate; leave blank for non-candidate or non-federal candidate")
    federal_district =  models.CharField(max_length=31, blank=True, null=True, help_text="US House district, if applicable")
    raw_name_guess = models.CharField(max_length=255, blank=True, null=True, help_text="raw candidate name, picked by computer. Possibly not right.")
    in_document_cloud = models.NullBooleanField(default=False, help_text="Has this been saved to document cloud and created as an ad buy?")
    dc_slug = models.CharField(max_length=255, blank=True, null=True, help_text="Document cloud slug")
    dc_title = models.CharField(max_length=255, blank=True, null=True, help_text="Document cloud title")
    # flattened fields, for efficient pages:
    nielsen_dma = models.CharField(max_length=60, blank=True, null=True, help_text='Nielsen Designated Market Area')
    dma_id = models.PositiveIntegerField(blank=True, null=True, editable=False, help_text='DMA ID, from Nielsen')
    community_state = models.CharField(max_length=7, blank=True, null=True)

    is_backed_up =  models.NullBooleanField(default=False, help_text="Has this been saved to S3")
    local_file_path =  models.CharField(max_length=511, blank=True, null=True, help_text='local file path')
    s3_full_url = models.CharField(max_length=600, blank=True, null=True, help_text='s3 url')
    not_at_fcc = models.NullBooleanField(default=False, help_text="Has the file gone missing?")
    missing_as_of_date = models.DateTimeField(blank=True, null=True, auto_now=False, help_text="When did we first notice the file was missing?")
    paths_configured = models.NullBooleanField(default=False, help_text="Have we guessed file paths that we can guess?")
    
    ## 2016 HACK FOR NEW API
    fcc_file_id = models.CharField(max_length=40, blank=True, null=True, help_text='36-digit hash from FCC API')
    folder_id = models.CharField(max_length=40, blank=True, null=True, help_text='36-digit hash from FCC API')
    file_manager_id = models.CharField(max_length=40, blank=True, null=True, help_text='36-digit hash from FCC API')
    download_url = models.CharField(max_length=255, blank=True, null=True, help_text='link to actually download file')
    file_status = models.CharField(max_length=31, blank=True, null=True)
    history_status = models.CharField(max_length=31, blank=True, null=True)
    
    def path(self):
        return get_file_path(self.raw_url)
    def folder_name(self):
        rawpath = get_file_path(self.raw_url)
        return ":".join(rawpath[1:-1])
    def file_name(self):
        if self.download_url:
            rawpath = get_file_path(self.raw_url)
            return (rawpath[-1:][0])
        else:
            parts = self.raw_url.split('Political File')
            url_bits = parts[-1].split("/")
            url_bits.reverse()
            return "-".join(url_bits)

        
    def search_text(self):
        rawpath = get_file_path(self.raw_url)
        if rawpath:
            return " ".join(rawpath[1:])
        rawpath = get_file_path(self.underscore_url)
        if rawpath:
            return " ".join(rawpath[1:])
        else:
            parts = self.raw_url.split('Political File')
            url_bits = parts[-1].split("/")
            url_bits.reverse()
            return "-".join(url_bits)
        
    def candidate_type(self):
        if self.federal_office:
            return self.federal_office
        else:
            if self.ad_type:
                return self.ad_type
        return " "
     
    def __unicode__(self):
        return self.search_text()
        
    def get_absolute_url(self):
        return "/fcc/r/%s/" % self.pk

class state_summary(models.Model):
    state_id = models.CharField(max_length=2, blank=True, null=True)
    num_broadcasters = models.PositiveIntegerField(blank=True, null=True, help_text="only mandated broadcasters")
    tot_buys = models.PositiveIntegerField(blank=True, null=True)
    pres_buys =  models.PositiveIntegerField(blank=True, null=True)
    sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    house_buys =  models.PositiveIntegerField(blank=True, null=True)
    state_buys = models.PositiveIntegerField(blank=True, null=True)
    local_buys = models.PositiveIntegerField(blank=True, null=True)
    outside_buys = models.PositiveIntegerField(blank=True, null=True)
    recent_pres_buys =  models.PositiveIntegerField(blank=True, null=True)  
    recent_sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_house_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_outside_buys = models.PositiveIntegerField(blank=True, null=True)
    
    def get_absolute_url(self):
        return "/fcc/by-state/%s/" % (self.state_id)
        
    def get_station_url(self):
        return "/fcc/stations/state/%s/" % (self.state_id)  

    def name(self):
        return STATES_DICT[self.state_id]
    

class dma_summary(models.Model):
    dma_id = models.PositiveIntegerField(blank=True, null=True, editable=False, help_text='DMA ID, from Nielsen')
    dma_name = models.CharField(max_length=255, blank=True, null=True, help_text="Better name - set from file")
    fcc_dma_name = models.CharField(max_length=255, blank=True, null=True)
    rank1011 = models.PositiveIntegerField(blank=True, null=True)
    rank1112 = models.PositiveIntegerField(blank=True, null=True)
    
    num_broadcasters = models.PositiveIntegerField(blank=True, null=True, help_text="only mandated broadcasters")
    tot_buys = models.PositiveIntegerField(blank=True, null=True)
    pres_buys =  models.PositiveIntegerField(blank=True, null=True)
    sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    house_buys =  models.PositiveIntegerField(blank=True, null=True)
    state_buys = models.PositiveIntegerField(blank=True, null=True)
    local_buys = models.PositiveIntegerField(blank=True, null=True)
    outside_buys = models.PositiveIntegerField(blank=True, null=True)
    recent_pres_buys =  models.PositiveIntegerField(blank=True, null=True)  
    recent_sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_house_buys =  models.PositiveIntegerField(blank=True, null=True)
    recent_outside_buys = models.PositiveIntegerField(blank=True, null=True)
    
    def get_absolute_url(self):
        return "/fcc/by-dma/%s/" % (self.dma_id)
        
    def get_station_url(self):
        return "/fcc/stations/dma/%s/" % (self.dma_id)
    
    def name(self):
        return self.dma_name


class dma_weekly(models.Model):
    # what day did the week start? 
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    
    # This is the week number in terms of the isocalendar week number--weeks end on sunday. 
    # (year, week, day) = datetime.date(2014,3,5).isocalendar()
    # cycle_week_number = (52*(year-2013)) + week
    cycle_week_number = models.IntegerField(null=True, blank=True)    
    
    dma_id = models.PositiveIntegerField(blank=True, null=True, editable=False, help_text='DMA ID, from Nielsen')
    dma_name = models.CharField(max_length=255, blank=True, null=True, help_text="Better name - set from file")
    fcc_dma_name = models.CharField(max_length=255, blank=True, null=True)
    
    tot_buys = models.PositiveIntegerField(blank=True, null=True)
    pres_buys =  models.PositiveIntegerField(blank=True, null=True)
    sen_buys =  models.PositiveIntegerField(blank=True, null=True)
    house_buys =  models.PositiveIntegerField(blank=True, null=True)
    state_buys = models.PositiveIntegerField(blank=True, null=True)
    local_buys = models.PositiveIntegerField(blank=True, null=True)
    outside_buys = models.PositiveIntegerField(blank=True, null=True)
    

    def get_absolute_url(self):
        return "/political-files/dma/%s/" % (self.dma_id)
    
    def get_station_url(self):
        return "/political-files/stations/dma/%s/" % (self.dma_id)

    def name(self):
        return self.dma_name
