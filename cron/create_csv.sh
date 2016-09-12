#!/bin/bash
NAME=fccpoliticalads
PROJ=fccpoliticalads 

# activate our env
source /projects/$NAME/virt/bin/activate
# Did we really activate it? 
echo "Virtual env set to: " $VIRTUAL_ENV

# psql copy local command ; requires .pgpass file to be correctly set
psql -h 10.210.246.176 -p 5433 -U fccpoliticalads -d politicaladsleuth -f /projects/fccpoliticalads/bin/adsleuth_export.sql
# special for philly. 
psql -h 10.210.246.176 -p 5433 -U fccpoliticalads -d politicaladsleuth -f /projects/fccpoliticalads/bin/adsleuth_philly_export.sql

# move file to correct place
python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py move_bulkfile_to_s3

