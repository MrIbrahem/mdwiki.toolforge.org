#!/usr/bin/python

"""

python pwb.py mdwiki/py/check


python3 pwb.py py/check

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import urllib
import codecs
#---
#from pywikibot import textlib
#---
import re
import string
import time
import sys
import pywikibot
import os
import urllib
import urllib.request
import urllib.parse
#---
sys_argv = sys.argv or []
#---
import mdwiki_api



#---
import py_tools
# py_tools.split_lists_to_numbers( list, maxnumber = 100 )
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project += '/public_html/Translation_Dashboard/Tables/'
#---
import wdapi
# wdapi.submitAPI( params, apiurl = 'https://' + 'www.wikidata.org/w/api.php', returnjson = False )
# wdapi.submitAPI_token( params, apiurl = 'https://' + 'www.wikidata.org/w/api.php', returnjson = False )
#---
medwiki_to_enwiki_conflic = {}
medwiki_to_enwiki = {}
missing_in_enwiki = []
sames = []
#---
def check():
    #---
    pywikibot.output('Get cat pages from cat : RTT' )
    Listo = mdwiki_api.subcatquery( 'RTT', depth = '1', ns = '0' )
    pywikibot.output('len of cat pages: %d' % len(Listo) )
    #---
    number = 0
    #---
    Listo = [ x for x in Listo if not ( x.startswith('Category:') or x.startswith('File:') or x.startswith('Template:') or x.startswith('User:') or x.endswith("(disambiguation)") ) ]
    #---
    splits = py_tools.split_lists_to_numbers( Listo, maxnumber = 150 )
    #---
    for numbb in splits :
        #---
        newlist = splits[numbb]
        #---
        line = "|".join( newlist )
        #---
        #pywikibot.output(line)
        #---
        params = {
            "action": "query",
            "format": "json",
            
            #"prop": "redirects",
            #"rdlimit": "max"
            
            "titles": line,
            "redirects": 1,
            "converttitles": 1,
            "utf8": 1,
        }
        #---
        #jsone = mdwiki_api.post( params )
        jsone = wdapi.submitAPI( params, apiurl = 'https://' + 'en.wikipedia.org/w/api.php', returnjson = False )
        #---
        if jsone and 'batchcomplete' in jsone:
            #---
            query = jsone.get( "query", {} )
            #---
            # "redirects": [{"from": "Acetylsalicylic acid","to": "Aspirin"}]
            Redirects = query.get( "redirects", [] )
            for red in Redirects:
                if not red["to"] in Listo:
                    medwiki_to_enwiki[red["from"]] = red["to"]
                else:
                    medwiki_to_enwiki_conflic[red["from"]] = red["to"]
            #---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get( "pages", {} )
            #---
            pages_example = {
            "-1": {
                "ns": 0,
                "title": "Fsdfdsf",
                "missing": ""
                },
            "2767": {
                "pageid": 2767,
                "ns": 0,
                "title": "ACE inhibitor"
                }
            }
            #---
            for page in pages:
                #---
                tab = pages[page]
                title = tab['title']
                #---
                if 'missing' in tab : 
                    missing_in_enwiki.append(title)
                else:
                    #pywikibot.output('<<lightyellow>> title["%s"] sames' % title )
                    sames.append(title)
            #---
        else:
            pywikibot.output( "<<lightred>> check.py no jsone" )
            pywikibot.output( jsone )
        #---
        #break
        #---
    #---
    numb = 0
    for fromm, to in medwiki_to_enwiki.items():
        numb += 1
        faf = '["%s"]' % fromm
        pywikibot.output('en titles %d from_to%s = "%s"' % (numb, faf.ljust(30), to ) )
    #---
    numb = 0
    for mis in missing_in_enwiki:
        numb += 1
        pywikibot.output('<<lightyellow>> %d title:%s missing_in_enwiki' % (numb, mis.ljust(25) ) )
    #---
    numb = 0
    #---
    for md, en in medwiki_to_enwiki_conflic.items():
        numb += 1
        faf = '["%s"]' % md
        fen = '["%s"]' % en
        pywikibot.output('<<lightred>> %d page%s redirect to enwiki%s, and they both in mdwiki cat.' % ( numb, faf.ljust(30), fen.ljust(30) ) )
    #---
    pywikibot.output('<<lightgreen>> len of medwiki_to_enwiki:%d' % ( len(medwiki_to_enwiki) ) )
    pywikibot.output('<<lightgreen>> len of missing_in_enwiki:%d' % ( len(missing_in_enwiki) ) )
    pywikibot.output('<<lightgreen>> len of medwiki_to_enwiki_conflic:%d' % ( len(medwiki_to_enwiki_conflic) ) )
    pywikibot.output('<<lightgreen>> len of sames:%d' % ( len(sames) ) )
    #---
    # ?????????????? ?????? ??????????????
    with open( project + 'medwiki_to_enwiki.json', 'w' ) as f1:
        json.dump( medwiki_to_enwiki, f1 )
    f1.close()
    #---
    with open( project + 'missing_in_enwiki.json', 'w' ) as f1:
        json.dump( missing_in_enwiki, f1 )
    f1.close()
    #---
    with open( project + 'sames.json', 'w' ) as f1:
        json.dump( sames, f1 )
    f1.close()
#---
if __name__ == '__main__':
    check()
#---
