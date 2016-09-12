NAME=fccpoliticalads
PROJ=fccpoliticalads
LOGFILE=/mnt/cron-log-backup

# activate our env
source /projects/$NAME/virt/bin/activate

echo "====== RUN START === $(date --rfc-3339=date) ======" >> $LOGFILE
/projects/fccpoliticalads/virt/bin/python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py backup_local >> $LOGFILE
/projects/fccpoliticalads/virt/bin/python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py push_backups_to_S3 >> $LOGFILE

