from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from fecdata.models import Candidate

from django.conf import settings
FEC_DATA_DIR = getattr(settings, 'FEC_DATA_DIR')



class Command(BaseCommand):
    args = '<cycle>'
    help = "Populate the candidates table from the candidate master file. Use a 2-digit cycle"
    requires_model_validation = False
    
    def handle(self, *args, **options):
        cycle = args[0]
        cycle_year = 2000 + int(cycle)
        assert cycle, "You must enter a two-digit cycle"
        
        fields = [('fec_id', (1, 9)),
                  ('fec_name', (10, 47)),
                  ('party', (48, 50)),
                  ('seat_status', (57, 57)),
                  ('candidate_status', (59, 59)),
                  ('state_address', (146, 147)),
                  ('zipcode', (148, 152)),
                  ('campaign_comm', (153, 161)),
                  ('election_year', (162, 163)),
                  ('current_district', (164, 165)), ]

        data_filename = "%s/%s/cn.txt" % (FEC_DATA_DIR, cycle)
        data_file = open(data_filename, "r")
        for line in data_file:
            line = line.replace("\n","")
            columns = line.split("|")
            data_dict = {}
            

            data_dict['fec_id'] = columns[0].strip()
            data_dict['fec_name'] = columns[1].strip()            
            data_dict['party'] = columns[2].strip()
            data_dict['election_year'] = columns[3].strip()
            data_dict['state_race'] = columns[4].strip()
            data_dict['office'] = columns[5].strip()
            data_dict['district'] = columns[6].strip()                                                            
            data_dict['seat_status'] = columns[7].strip() 
            data_dict['candidate_status'] = columns[8].strip()
            data_dict['campaign_com_fec_id'] = columns[9].strip()
            data_dict['zipcode'] = columns[14].strip()

            #print data_dict
                
            try:
                existing_candidate = Candidate.objects.get(fec_id=data_dict['fec_id'], cycle=cycle_year)
            except Candidate.DoesNotExist:
                
                
                # office is the first digit of the fec_id (?)
                office = data_dict['fec_id'][0]
                # state race is the next two digits

                
                print "Adding candidate with name: %s id: %s" % (data_dict['fec_name'], data_dict['fec_id'])
                Candidate.objects.create(
                            cycle=cycle_year,
                            fec_id=data_dict['fec_id'],
                            fec_name=data_dict['fec_name'],
                            party=data_dict['party'],
                            office=office,
                            seat_status=data_dict['seat_status'],
                            candidate_status=data_dict['candidate_status'],
                            state_race=data_dict['state_race'],
                            district=data_dict['district'],
                            campaign_com_fec_id=data_dict['campaign_com_fec_id']
                            
                                        )
                
                
        