NAME=fccpoliticalads
PROJ=fccpoliticalads

# activate our env
source /projects/$NAME/virt/bin/activate

python /projects/fccpoliticalads/src/fcc_political_ads/fcc_adtracker/manage.py export_adbuys_to_S3 -b

