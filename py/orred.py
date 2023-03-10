#!/usr/bin/python


"""

إنشاء تحويلات من العنوان الإنجليزي
إلى العنوان المحلي
في orwiki

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import codecs
import pywikibot
import re
import string
import time
import sys
#---
sys_argv = sys.argv or []
#---
import urllib
import urllib.request
import urllib.parse
from pywikibot import config
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
#---
import wpref
# wpref.submitAPI( params , lang = 'or' , returnjson = False )
#---
or_url = 'https://' + 'or.wikipedia.org/w/api.php'
#---
def Find_pages_exists_or_not( liste , apiurl = '' ) :
    #---
    params = {
        "action": "query",
        "format": "json",
        "titles": '|'.join( liste ),
        #"redirects": 0,
        #"prop": "templates|langlinks",
        "utf8": 1,
        "token" : ""
    }
    #---
    table = {}
    #---
    json1 = wpref.submitAPI( params, lang = 'or')
    #---
    if json1:
        query_pages = json1.get("query",{}).get("pages",{})
        for page in query_pages:
            kk = query_pages[page]
            faso = ''
            if "title" in kk:
                tit = kk.get("title","")
                #---
                if "missing" in kk:
                    table[tit] = False
                else:
                    table[tit] = True
        #---
    return table
#---
def create_redirect( target, mdtitle ):
    #---
    pywikibot.output( '----------\n*<<lightyellow>> >target:"%s".' % target )
    #---
    exists = Find_pages_exists_or_not( [target,mdtitle] , apiurl = or_url )
    #---
    Worrk = False
    #---
    for tit , o in exists.items() :
        if o == False:
            if tit.lower() == target.lower() :
                pywikibot.output( " target:%s not exists in orwiki." % target )
                return ""
            elif tit.lower() == mdtitle.lower() :
                Worrk = True
    #---
    if Worrk :
        #---
        text = '#redirect [[%s]]' % target
        sus = 'Redirected page to [[%s]]' % target
        params = {
            "action": "edit",
            "format": "json",
            "title": mdtitle,
            "text": text,
            "summary": sus,
            "createonly": 1,
            "utf8": 1,
            "token": ""
        }
        #---
        uu = wpref.submitAPI( params, lang = 'or')
        #---
        if 'Success' in uu :
            pywikibot.output('<<lightgreen>>** true .. [[%s]] ' % mdtitle )
        else:
            pywikibot.output( uu )
#---
def dodo_sql():
    #---
    que = '''
select title,target from pages
where target != ""
and lang = "or"
;
'''
    #---
    sq = sql_for_mdwiki.mdwiki_sql(que)
    #---
    for tab in sq :
        mdtitle  = tab[0]
        target   =  tab[1]
        #---
        create_redirect( target , mdtitle )
#---
# python3 pwb.py py/orred
#---
if __name__ == "__main__":
    dodo_sql()
#---
