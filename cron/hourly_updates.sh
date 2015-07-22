NAME=fccpoliticalads
PROJ=fccpoliticalads
LOGFILE=/mnt/cron-log-hourly

# activate our env
source /projects/$NAME/virt/bin/activate


echo "====== RUN START === $(date --rfc-3339=date) ======" >> $LOGFILE

# sets markets on uploaded documents
echo 'cleanup adbuys'
/projects/fccpoliticalads/virt/bin/python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py cleanup_adbuys >> $LOGFILE 
# summarize stats by dma
echo 'summarize buys'
/projects/fccpoliticalads/virt/bin/python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py summarize_buys >> $LOGFILE
echo 'summarize weekly'
/projects/fccpoliticalads/virt/bin/python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py summarize_weekly >> $LOGFILE
# reset index:
echo 'resetting elastic search indexes'
/projects/fccpoliticalads/virt/bin/python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py update_index --age=24 >> $LOGFILE
