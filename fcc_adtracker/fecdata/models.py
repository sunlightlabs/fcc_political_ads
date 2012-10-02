import re

from django.db import models
from django.contrib.localflavor.us.us_states import STATE_CHOICES

STATE_CHOICES = dict(STATE_CHOICES)

type_hash={'C': 'Communication Cost',
          'D': 'Delegate',
          'H': 'House',
          'I': 'Not a Committee',
          'N': 'Non-Party, Non-Qualified',
          'P': 'Presidential',
          'Q': 'Qualified, Non-Party',
          'S': 'Senate',
          'X': 'Non-Qualified Party',
          'Y': 'Qualified Party',
          'Z': 'National Party Organization',
          'E': 'Electioneering Communication',
          'O': 'Super PAC'
          }
    
# populated from fec's candidate master
class Candidate(models.Model):
    cycle = models.CharField(max_length=4)
    fec_id = models.CharField(max_length=9, blank=True)
    fec_name = models.CharField(max_length=255) 
    party = models.CharField(max_length=3, blank=True)
    office = models.CharField(max_length=1,
                            choices=(('H', 'House'), ('S', 'Senate'), ('P', 'President'))
                            )
    seat_status = models.CharField(max_length=1,
                                choices=(('I', 'Incumbent'), ('C', 'Challenger'), ('O', 'Open'))
                                )
    candidate_status = models.CharField(max_length=1,
                                      choices=(('C', 'STATUTORY CANDIDATE'), ('F', 'STATUTORY CANDIDATE FOR FUTURE ELECTION'), ('N', 'NOT YET A STATUTORY CANDIDATE'), ('P', 'STATUTORY CANDIDATE IN PRIOR CYCLE'))
                                       )
    # state is from the candidate's address (?)                                     
    state_address = models.CharField(max_length=2, blank=True)    
    district = models.CharField(max_length=2, blank=True)
    # the state where the race is taking place (from the candidate id)
    state_race = models.CharField(max_length=2, blank=True, null=True) 
    campaign_com_fec_id = models.CharField(max_length=9, blank=True)

def race(self):

      if self.office == 'P':
          return 'President' 
      elif self.office == 'S' or self.district.startswith('S'):
          return '%s (Senate)' % self.fec_id[2:4]
      else:
          return '%s-%s (House)' % (self.fec_id[2:4], self.district.lstrip('0'))

# Populated from fec's committee master            
class Committee(models.Model):
    name = models.CharField(max_length=255)
    fec_id = models.CharField(max_length=9, blank=True)
    slug = models.SlugField(max_length=100)
    party = models.CharField(max_length=3, blank=True)
    # Josue Larose has 62 pacs and counting... 
    treasurer = models.CharField(max_length=38, blank=True, null=True)
    street_1 = models.CharField(max_length=34, blank=True, null=True)
    street_2 = models.CharField(max_length=34, blank=True, null=True)
    city = models.CharField(max_length=18, blank=True, null=True)
    zip_code = models.CharField(max_length=9, blank=True, null=True)
    state_race = models.CharField(max_length=2, blank=True, null=True)
    designation = models.CharField(max_length=1,
                                 blank=False,
                                 null=True,
                                 choices=[('A', 'Authorized by Candidate'),
                                          ('J', 'Joint Fund Raiser'),
                                          ('P', 'Principal Committee of Candidate'),
                                          ('U', 'Unauthorized'),
                                          ('B', 'Lobbyist/Registrant PAC'),
                                          ('D', 'Leadership PAC')])

    ctype = models.CharField(max_length=1,
                           blank=False,
                           null=True,
                           choices=[('C', 'Communication Cost'),
                                    ('D', 'Delegate'),
                                    ('H', 'House'),
                                    ('I', 'Independent Expenditure (Not a Committee'),
                                    ('N', 'Non-Party, Non-Qualified'),
                                    ('P', 'Presidential'),
                                    ('Q', 'Qualified, Non-Party'),
                                    ('S', 'Senate'),
                                    ('X', 'Non-Qualified Party'),
                                    ('Y', 'Qualified Party'),
                                    ('Z', 'National Party Organization'),
                                    ('E', 'Electioneering Communication'),
                                    ('O', 'Super PAC') ])

    tax_status = models.CharField(max_length=10,
          choices=(('501(c)(4)', '501(c)(4)'),
                   ('501(c)(5)', '501(c)(5)'),
                   ('501(c)(6)', '501(c)(6)'),
                   ('527', '527'),
                   ('FECA PAC', 'FECA PAC'),
                   ('FECA Party', 'FECA Party'),
                   ('Person', 'Person'),
          ),
          blank=True, null=True)
    filing_frequency = models.CharField(max_length=1, 
          choices=[('A', 'ADMINISTRATIVELY TERMINATED'),
                   ('D', 'DEBT'),
                   ('M', 'MONTHLY FILER'),
                   ('Q', 'QUARTERLY FILER'),
                   ('T', 'TERMINATED'),
                   ('W', 'WAIVED')
                   ])
    interest_group_cat= models.CharField(max_length=1,choices=[
                          ('C', 'CORPORATION'),
                          ('L', 'LABOR ORGANIZATION'),
                          ('M', 'MEMBERSHIP ORGANIZATION'),
                          ('T', 'TRADE ASSOCIATION'),
                          ('V', 'COOPERATIVE'),
                          ('W', 'CORPORATION WITHOUT CAPITAL STOCK')
                        ])
    connected_org_name=models.CharField(max_length=65, blank=True)
    candidate_id = models.CharField(max_length=9,blank=True)
    candidate_office = models.CharField(max_length=1, blank=True)

    # Fields set from fec lists after the fact
    is_superpac = models.NullBooleanField(null=True, default=False)    
    is_hybrid = models.NullBooleanField(null=True, default=False)  
    is_nonprofit = models.NullBooleanField(null=True, default=False)

    # related candidate, if there is one. From the candidate_id only. 
    related_candidate = models.ForeignKey(Candidate, null=True) 

    def get_fec_url(self):
      url = "http://query.nictusa.com/cgi-bin/dcdev/forms/%s/" % (self.fec_id)
      return url

    def set_candidate(self):
      try:
          this_candidate = Candidate.objects.get(fec_id=self.candidate_id)
          self.related_candidate = this_candidate
          self.save()
          return True
          
      except Candidate.DoesNotExist:
          return False

    def display_type(self):
      key = self.ctype
      try:
          return type_hash[key]
      except KeyError:
          return ''

