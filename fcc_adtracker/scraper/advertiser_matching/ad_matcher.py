import re
from fccpublicfiles.models import Organization, TV_Advertiser

# Conservative match assumptions, generally. 

regex_array = [
    {'advertiser_name':'PRIORITIES USA ACTION',
    'candidate_type':re.compile('[Non\-Candidate Issue Ads|President]'), 
    'regexes': [re.compile('PRIORITIES\s*U\s*S\s*A'), re.compile('PRIORITES\s*U\s*S\s*A')],
    },
    # MANY ADS DON'T SPECIFY WHETHER THEY'RE THE SUPER PAC OR THE C4. 
    {'advertiser_name':'AMERICAN CROSSROADS',
    'candidate_type':re.compile('.'), 
    'regexes': [re.compile('^AMERICAN CROSSROADS'), re.compile('^AM CROSSROADS'), re.compile('^AMER CROSSROADS'), re.compile('^AMRCN CROSSROADS')],
    },
    {'advertiser_name':'Crossroads GPS',
    'candidate_type':re.compile('.'), 
    'regexes': [re.compile('^CROSSROADS GPS'), re.compile('^CROSSROADS GRASSROOTS')],
    },
    {'advertiser_name':'RESTORE OUR FUTURE, INC.',
    'candidate_type':re.compile('[Non\-Candidate Issue Ads|President]'), 
    'regexes': [re.compile('RESTORE\s*OUR\s*FUTURE')],
    },
    {'advertiser_name':'DEMOCRATIC CONGRESSIONAL CAMPAIGN COMMITTEE',
    'candidate_type':re.compile('.'), 
    'regexes': [re.compile('^DCCC'), re.compile('DEMOCRATIC CONGRESSIONAL CAMPAIGN COMMITTEE')],
    },
    {'advertiser_name':'NATIONAL REPUBLICAN CONGRESSIONAL COMMITTEE',
    'candidate_type':re.compile('.'), 
    'regexes': [re.compile('^NRCC'), re.compile('NATIONAL REPUBLIC CAMPAIGN COMMITTEE')],
    },
    {'advertiser_name':'NATIONAL REPUBLICAN SENATORIAL COMMITTEE',
    'candidate_type':re.compile('.'), 
    'regexes': [re.compile('^NRSC'), re.compile('NATIONAL REPUBLICAN SENATORIAL COMMITTEE')],
    },
    {'advertiser_name':'DEMOCRATIC SENATORIAL CAMPAIGN COMMITTEE',
    'candidate_type':re.compile('.'), 
    'regexes': [re.compile('^DSCC'), re.compile('DEMOCRATIC SENATORIAL CAMPAIGN COMMITTEE')],
    },
    {'advertiser_name':'AMERICANS FOR PROSPERITY',
    'candidate_type':re.compile('.'), 
    'regexes': [re.compile('^AFP'), re.compile('AMERICANS FOR PROSPERITY'), re.compile('AMER FOR PROSPER'), re.compile('AMER 4 PROSPER')],
    },
    {'advertiser_name':'MAJORITY PAC',
    'candidate_type':re.compile('.'), 
    'regexes': [re.compile('^MAJORITY PAC')],
    },
    # put these last, b/c the text romney or obama often appears in non candidate ads erroneously put in the president folder.
    {'advertiser_name':'ROMNEY FOR PRESIDENT INC.',
    'candidate_type':re.compile('President'), 
    'regexes': [re.compile('ROMNEY')],     
    },
    {'advertiser_name':'OBAMA FOR AMERICA',
    'candidate_type':re.compile('President'), 
    'regexes': [re.compile('OBAMA')],
    },
]



    
    
class ad_matcher(object):


    def __init__(self):
        print "starting ad matcher..."
        self.interpreted_regex_array = []

        for item in regex_array:
            advertiser_name = item['advertiser_name']
            advertiser = Organization.objects.get(organization_type='AD', related_advertiser__advertiser_name__iexact =advertiser_name)
            print "got advertiser from name=%s" % (advertiser_name)
            this_array_item = item
            this_array_item['advertiser'] = advertiser
            self.interpreted_regex_array.append(this_array_item)
    
    def match_name(self, url_string, this_can_type):
        for item in self.interpreted_regex_array:
            if re.search(item['candidate_type'], this_can_type):
                for regex in item['regexes']:
                    if re.search(regex, url_string):
                        return item['advertiser']
            else: 
                continue
        return None
    # 

