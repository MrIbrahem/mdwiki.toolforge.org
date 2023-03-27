#!/usr/bin/python

"""
بوت قواعد البيانات
"""
#
# (C) Ibrahem Qasim, 2022
#
#
from pywikibot import config
import re
import json
import codecs
from warnings import warn
import pywikibot
import string
import sys
import urllib
import urllib.request
import urllib.parse
#---
import time as tttime
import datetime
from datetime import datetime#, date, time
#---
TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
#---
can_use_sql_db  = { 1 : False }
SQL_Ready  = False
#---
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
#---
try:
    import MySQLdb
    SQL_Ready = True
    can_use_sql_db[1] = True
except Exception as e:
    pywikibot.output('<<lightred>> mdwiki/mdpy/wiki_sql.py errors when import MySQLdb ')
    pywikibot.output('<<lightred>> %s ' % e)
#---
'''
#---
import wiki_sql
# wiki_sql.GET_SQL()
# wiki_sql.Make_sql_many_rows( queries , wiki="", printqua = False)
#---
'''
#---
def GET_SQL():
    return can_use_sql_db[1]
#---        
content_lang_map = {
    "be-x-old" : "be-tarask",
    "be_x_old" : "be-tarask",
    "bh" : "bho",
    "crh" : "chr-latn",
    "no" : "nb",
    "als"	:	"gsw",
    "bat-smg"	:	"sgs",
    "cbk-zam"	:	"cbk",
    "eml"	:	"egl",
    "fiu-vro"	:	"vro",
    "map-bms"	:	"jv-x-bms",
    "nrm"	:	"nrf",
    "roa-rup"	:	"rup",
    "roa-tara"	:	"nap-x-tara",
    "simple"	:	"en-simple",
    "zh-classical"	:	"lzh",
    "zh-min-nan"	:	"nan",
    "zh-yue"	:	"yue",
}
#---
def make_labsdb_dbs_p(wiki):
    #---
    lang = wiki
    #---
    if lang.endswith('wiki') : lang = lang[:-4]
    #---
    if lang in content_lang_map:
        wiki = content_lang_map[lang]
    #---
    wiki = f"{wiki}wiki"
    dbs = wiki
    #---
    host = "%s.analytics.db.svc.wikimedia.cloud" % wiki
    #---
    dbs_p = dbs + '_p'
    #---
    _host_    =   config.db_hostname_format.format(wiki)
    if host != _host_:
        pywikibot.output(f'<<lightyellow>>host:{host} != _host:{_host_}')
    #---
    _dbs_p_   =   config.db_name_format.format(wiki) + '_p'
    #---
    if dbs_p != _dbs_p_:
        pywikibot.output(f'dbs_p:{dbs_p} != _dbs_p:{_dbs_p_}')
    #---
    return host, dbs_p
#---
def Make_sql_many_rows(queries, wiki="", printqua=False):
    rows = []
    #---
    pywikibot.output( "wiki_sql.py Make_sql_many_rows wiki '%s'" % wiki )
    #---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    #---
    if printqua or "printsql" in sys.argv:
        pywikibot.output( queries )
    #---
    if not GET_SQL():
        pywikibot.output( 'sql.GET_SQL() == False' )
        return rows
    #---
    start = tttime.time()
    final = tttime.time()
    #delta = int(final - start)
    #pywikibot.output( 'wiki_sql.py Make_sql len(encats) = "{}", in {} seconds'.format( len( encats ) , delta)  )
    #---
    db_user = config.db_username
    dpas    = config.db_password
    #---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    #---
    # pywikibot.output( '<<lightred>> wiki_sql.py <<lightyellow>>host:"%s" , db:"%s" , db_user:"%s" %s' % (host , dbs_p , db_user , TTime) )
    #---
    if SQL_Ready:
        #---
        # MySQLdb.connect with arrgs
        arrgs = {
            'host': host,
            'user': db_user,
            'passwd': dpas,
            'db': dbs_p,
        }
        #---
        # connect to the database server without error
        try:
            cn = MySQLdb.connect(**arrgs)
        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return rows
        #---
        cn.set_character_set('utf8')
        cur = cn.cursor()
        #---
        # cur.execute(queries)
        # skip sql errors
        try:
            cur.execute(queries)
        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( queries )
            pywikibot.output( 'CRITICAL:' )
            return rows
        #---
        en_results = cur.fetchall()
        cn.close()
        # -----------------
        final = tttime.time()
        # -----------------end of sql--------------------------------------------
        for raw in en_results:
            #if type(raw) == bytes:
                #raw = raw.decode("utf-8")
            raw2 = raw
            if type(raw2) == list or type(raw2) == tuple :
                raw = [ py_tools.Decode_bytes(x) for x in raw2 ]
            rows.append(raw)
    # -----------------
    else:
        pywikibot.output("no SQL_Ready" )
    # -----------------
    delta = int(final - start)
    pywikibot.output( 'wiki_sql.py Make_sql_many_rows len(encats) = "{}", in {} seconds'.format( len( rows ) , delta)  )
    # -----------------
    return rows
#---
