import re
import urllib2

from urlparse import urlparse

from django.conf import settings

from doccloud.models import Document
from django.contrib.auth.models import User
from django.core.files import File


SCRAPER_USER_AGENT_STRING = getattr(settings, 'SCRAPER_USER_AGENT_STRING', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7')


def read_url(url):
    # read url with our headers.
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', SCRAPER_USER_AGENT_STRING)]
    parsed_url = urlparse(url)
    final_url = "%s://%s%s" % (parsed_url.scheme, parsed_url.netloc, urllib2.quote(parsed_url.path))
    
    # deal with comma issue
    final_url = final_url.replace("%2C", ",")
    final_url = final_url.replace("%2c", ",")
    print("trying to read url: %s" % (final_url))
    page = opener.open(final_url).read()
    return page

# assumes we're looking at 2012
folder_url_re = re.compile(r'https://stations.fcc.gov/station-profile/(.*?)/political-files/browse->(.*)')
file_url_re = re.compile(r'https://stations.fcc.gov/collect/files/(\d+)/Political File/(.+)')

#https://stations.fcc.gov/station-profile/wpvi-tv/political-files/browse->2012->state->delaware->markell_for_delaware
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

# List of stations that are mandated--we think--to post their political files. ABC, NBC, CBS and Fox affiliates in the top 50 DMA's should be on this list. Unsure about: can stations be 'partial' affiliates, or have agreements with major networks that don't rise to level of formal affiliation? As of this writing stations are either 'all in' or 'all out'; other stations can voluntarily upload their files, but if so they are supposed to upload all of them. Not sure if this has been formalized.
mandated_stations = ['WABC-TV', 'WCBS-TV', 'WNBC', 'WNYW', 'KABC-TV', 'KCBS-TV', 'KNBC', 'KTTV', 'KWHY-TV', 'WBBM-TV', 'WFLD', 'WLS-TV', 'WMAQ-TV', 'WMGM-TV', 'KYW-TV', 'WCAU', 'WPVI-TV', 'WTXF-TV', 'KDFW', 'KTVT', 'KXAS-TV', 'WFAA', 'KGO-TV', 'KNTV', 'KPIX-TV', 'KTVU', 'WBZ-TV', 'WCVB-TV', 'WFXT', 'WHDH', 'WMUR-TV', 'WJLA-TV', 'WRC-TV', 'WTTG', 'WUSA', 'WHAG-TV', 'WAGA-TV', 'WGCL-TV', 'WSB-TV', 'WXIA-TV', 'KHOU', 'KPRC-TV', 'KRIV', 'KTRK-TV', 'WDIV-TV', 'WJBK', 'WWJ-TV', 'WXYZ-TV', 'KCPQ', 'KING-TV', 'KIRO-TV', 'KOMO-TV', 'KNAZ-TV', 'KNXV-TV', 'KPHO-TV', 'KPNX', 'KSAZ-TV', 'WFLA-TV', 'WFTS-TV', 'WTSP', 'WTVT', 'WWSB', 'KARE', 'KCCO-TV', 'KCCW-TV', 'KFTC', 'KMSP-TV', 'KRWF', 'KSAX', 'KSTP-TV', 'WCCO-TV', 'WFOR-TV', 'WPLG', 'WSVN', 'WTVJ', 'KCNC-TV', 'KDVR',  'KFCT', 'KMGH-TV', 'KREG-TV', 'KUSA', 'KQCK', 'WEWS-TV', 'WJW', 'WKYC', 'WOIO', 'WESH', 'WFTV', 'WKMG-TV', 'WOFL', 'WRDQ', 'KCRA-TV', 'KOVR', 'KTXL', 'KXTV', 'KDNL-TV', 'KMOV', 'KSDK', 'KTVI', 'WCSH', 'WGME-TV', 'WMTW', 'WPFO', 'KDKA-TV', 'WPGH-TV', 'WPXI', 'WTAE-TV', 'WNCN', 'WRAL-TV', 'WRAZ', 'WTVD', 'WBTV', 'WCCB', 'WCNC-TV', 'WSOC-TV', 'WISH-TV', 'WRTV', 'WTHR', 'WXIN', 'WBAL-TV', 'WBFF', 'WJZ-TV', 'WMAR-TV', 'KFMB-TV', 'KGTV', 'KNSD', 'KSWB-TV', 'WKRN-TV', 'WSMV-TV', 'WTVF', 'WZTV', 'WFSB', 'WTIC-TV', 'WTNH', 'WVIT', 'KCTV', 'KMBC-TV', 'KSHB-TV', 'WDAF-TV', 'WBNS-TV', 'WCMH-TV', 'WSYX', 'WTTE', 'KENV-DT', 'KVNV', 'KMYU', 'KSL-TV', 'KSTU', 'KTVX', 'KUTV', 'KGWR-TV', 'WDJT-TV', 'WISN-TV', 'WITI', 'WTMJ-TV', 'WXIX-TV', 'WCPO-TV', 'WKRC-TV', 'WLWT', 'KABB', 'KENS', 'KSAT-TV', 'WOAI-TV', 'WUGA-TV', 'WLOS', 'WHNS', 'WSPA-TV', 'WFLX', 'WPBF', 'WPEC', 'WPTV-TV', 'WBRC', 'WCFT-TV', 'WIAT', 'WJSU-TV', 'WVTM-TV', 'KLAS-TV', 'KSNV-DT', 'KTNV-TV', 'KVVU-TV', 'WGAL', 'WHP-TV', 'WHTM-TV', 'WPMT', 'WOOD-TV', 'WOTV', 'WWMT', 'WXMI', 'WZZM', 'WAVY-TV', 'WTKR', 'WVBT', 'WVEC', 'KFOR-TV', 'KOCO-TV', 'KOKH-TV', 'KWTV-DT', 'KREZ-TV', 'KASA-TV', 'KBIM-TV', 'KOAT-TV', 'KOB', 'KOBF', 'KOBR', 'KRQE', 'WFMY-TV', 'WGHP', 'WXII-TV', 'WXLV-TV', 'KBVO', 'KEYE-TV', 'KTBC', 'KVUE', 'KXAN-TV', 'WAVE', 'WDRB', 'WHAS-TV', 'WLKY-TV', 'WHBQ-TV', 'WMC-TV', 'WPTY-TV', 'WREG-TV', 'WAWS', 'WJXX', 'WTEV-TV', 'WTLV']

