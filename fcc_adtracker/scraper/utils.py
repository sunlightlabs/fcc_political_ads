import re

# assumes we're looking at 2012
folder_url_re = re.compile(r'https://stations.fcc.gov/station-profile/(.*?)/political-files/browse->(.*)')
file_url_re = re.compile(r'https://stations.fcc.gov/collect/files/(\d+)/Political File/(.+)')

def clean_path(url):
    url = url.replace('&gt;', '>')
    url = url.replace('%3e', '>')
    return url
    
def parse_folder_url(url):
    url = clean_path(url)
    url_parts = re.findall(folder_url_re, url)
    (callSign, pathArray) = (None, None)
    if url_parts:
        callSign = url_parts[0][0]
        path = url_parts[0][1]
        pathArray = path.split('->')
    else: 
        print "Couldn't parse folder file path %s" % (url)
        
    return callSign, pathArray

def get_folder_path(url):
    url = clean_path(url)
    (callSign, PathArray) = parse_folder_url(url)
    return PathArray
    
def parse_file_url(url):
    url_parts = re.findall(file_url_re, url)
    (fac_id, pathArray) = (None, None)
    if url_parts:
        fac_id = url_parts[0][0]
        path = url_parts[0][1]
        pathArray = path.split('/')
    else: 
        print "Couldn't parse file path %s" % (url)
        
    return fac_id, pathArray

def get_file_path(url):
    (fac_id, PathArray) = parse_file_url(url)
    return PathArray