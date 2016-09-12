#!/bin/bash
NAME=fccpoliticalads
PROJ=fcc_political_ads 

datadir=/projects/$NAME/src/$PROJ/fcc_adtracker/fecdata/data

for year in '12'
do
    echo "Getting files for: $year"

    # Master candidates file -- includes *all* candidates
    curl -o $datadir/$year/cn$year.zip ftp://ftp.fec.gov/FEC/20$year/cn$year.zip
    unzip -o $datadir/$year/cn$year.zip -d $datadir/$year

    sleep 1

    # Master committee file -- includes *all* committees
    curl -o $datadir/$year/cm$year.zip ftp://ftp.fec.gov/FEC/20$year/cm$year.zip
    unzip -o $datadir/$year/cm$year.zip -d $datadir/$year

done

# activate our env
source /projects/$NAME/virt/bin/activate
# Did we really activate it? 
echo "Virtual env set to: " $VIRTUAL_ENV

/projects/$NAME/src/$PROJ/fcc_adtracker/manage.py pop_candidates 12
/projects/$NAME/src/$PROJ/fcc_adtracker/manage.py pop_committees 12
