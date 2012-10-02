

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from fecdata.models import Committee, Candidate
from django.conf import settings
FEC_DATA_DIR = getattr(settings, 'FEC_DATA_DIR')

def parse_file(filename):
    records = []
    with file(filename, 'rU') as masterfile:
        for (line_num, line) in enumerate(masterfile, start=1):
            line = line.replace("\n","")
            columns = line.split("|")
            row = {}
            row['committee_id'] = columns[0]
            row['committee_name'] = columns[1]
            row['treasurer'] = columns[2][:38]
            row['street1'] = columns[3][:34]
            row['street2'] = columns[4][:34]
            row['city'] = columns[5][:18]
            row['state'] = columns[6]
            row['zipcode'] = columns[7][:9]
            row['designation'] = columns[8]
            row['type'] = columns[9]
            row['party'] = columns[10]
            row['filing_frequency'] = columns[11]
            row['interest_group_category'] = columns[12]                                                                                                                                    
            row['connected_org_name'] =  columns[13][:65]
            row['candidate_id'] =  columns[14]
            
            row['line_num'] = line_num                
            row['slug'] = slugify(row['committee_name'][:50])
            records.append(row)

            #print row

        print "%d records to process..." % len(records)

    return records

def get_or_create_committee(record):
    try:
        cmte = Committee.objects.get(fec_id=record['committee_id'])
        #print ">>Found committee  %s %s" % (record['committee_id'], record['committee_name'])
    except Committee.DoesNotExist:
        print "Creating committee %s %s" % (record['committee_id'], record['committee_name'])
        cmte = Committee.objects.create(
            name=record['committee_name'],
            slug=record['slug'],
            fec_id=record['committee_id'],
            party=record['party'],
            treasurer=record['treasurer'],
            street_1=record['street1'],
            street_2=record['street2'],
            city=record['city'],
            state_race=record['state'],
            zip_code=record['zipcode'],
            designation=record['designation'],
            ctype=record['type'],
            filing_frequency=record['filing_frequency'], 
            connected_org_name=record['connected_org_name'],
            candidate_id=record['candidate_id'],
            interest_group_cat = record['interest_group_category']
            )
            
        try: 
            rc = Candidate.objects.get(fec_id=record['candidate_id'])
            cmte.related_candidate = rc
            cmte.save()
        except Candidate.DoesNotExist:
            print "Missing candidate id %s -- maybe it's from a previous cycle?" % (record['candidate_id'])
            pass
            


class Command(BaseCommand):
    args = '<cycle>'
    help = "Populate the committees table from the committee master file. Use a 2-digit cycle"
    requires_model_validation = False
    
    def handle(self, *args, **options):
        cycle = args[0]
        cycle_year = 2000 + int(cycle)
        assert cycle, "You must enter a two-digit cycle"
        data_filename = "%s/%s/cm.txt" % (FEC_DATA_DIR, cycle)

        records = parse_file(data_filename)
        for record in records:
            get_or_create_committee(record)
            
      
