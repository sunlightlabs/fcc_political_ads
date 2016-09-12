#!/bin/bash
NAME=fccpoliticalads
PROJ=fccpoliticalads 

# activate our env
source /projects/$NAME/virt/bin/activate
# Did we really activate it? 
echo "Virtual env set to: " $VIRTUAL_ENV

# scrapes fcc
python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py scrape_fcc_rss
# resets the scrape time
python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py set_scraper_time
# make ad buys from new scraped documents - has better db query.
python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py publish_fcc_docs

