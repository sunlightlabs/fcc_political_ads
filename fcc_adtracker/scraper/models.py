

from django.db import models

from broadcasters.models import Broadcaster

from utils import get_folder_path, get_file_path


# Represents the basic info in a folder. Folders have types, parents, and children, but that's 'recoverable' from the 
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
    
class PDF_File(models.Model):
    callsign = models.CharField(max_length=12)
    facility_id = models.PositiveIntegerField(blank=True, null=True, unique=True, editable=False, help_text='FCC assigned id')
    folder = models.ForeignKey(Folder)
    raw_url = models.CharField(max_length=511, unique=True) # not url encoded
    size = models.CharField(max_length=31, blank=True, null=True) # how big is it in text?
    upload_time = models.DateTimeField(blank=True, null=True, auto_now=False, help_text="When was this folder last modified?")
    related_candidate_id = models.CharField(max_length=15, blank=True, null=True, help_text="FEC candidate id if this folder represents a candidate")
    related_pac_id = models.CharField(max_length=15, blank=True, null=True, help_text="FEC committee id if this folder represents a committee")

    ad_type = models.CharField(max_length=31, blank=True, null=True, help_text="Federal, State, Local, Non-candidate")
    federal_office =  models.CharField(max_length=31, blank=True, null=True, help_text="President, House, Senate; leave blank for non-candidate or non-federal candidate")
    federal_district =  models.CharField(max_length=31, blank=True, null=True, help_text="US House district, if applicable")
    raw_name_guess = models.CharField(max_length=255, blank=True, null=True, help_text="raw candidate name, picked by computer. Possibly not right.")
    in_document_cloud = models.NullBooleanField(default=False, help_text="Has this been saved to document cloud?")
    

    
    def path(self):
        return get_file_path(self.raw_url)
    
    def __unicode__(self):
        return self.raw_url