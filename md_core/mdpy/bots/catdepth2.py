#!/usr/bin/env python
# -*- coding: utf-8  -*-
#   himo
""" 

python3 pwb.py mdpy/catdepth2

"""
#
# (C) Ibrahem Qasim, 2022
#
#

import re
import json
from warnings import warn
#import pywikibot
import codecs
import string
import time
import os
import sys
import datetime
from datetime import datetime
#---
Day_History = datetime.now().strftime("%Y-%m-%d")
#---
project = '/data/project/mdwiki/'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
from mdpy.bots import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query, update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
#---
from mdpy.bots import mdwiki_api
#---
def Get_cat(enlink, print_url = False ): 
    #---
    # إيجاد categorymembers والتصانيف الفرعية لتصنيف
    #---
    #print(' Get_cat for %s' % (enlink) )
    #---
    if not enlink.startswith('Category:') :
        enlink = 'Category:' + enlink
    #---
    params = {
        "action": "query",
        "format": "json",
        "utf8": 1,

        "generator": "categorymembers",
        "gcmtitle": enlink,
        "gcmprop": "title",
        "gcmtype": "page|subcat",
        "gcmlimit": "max",

        "redirects": 1,
        #"prop": "templates",
        #"tllimit": "max",

        #"lllang": langcode,
        #"lllimit": "max",
    }
    #---
    #if "tempapi" not in sys.argv :
        #params["prop"] = "templates"
        #params["tllimit"] = "max"
    #---all
    # if ns == "0" or ns == "10" : params["gcmtype"] = "page"
    # elif ns == "14" : params["gcmtype"] = "subcat"
    # elif ns == "all" :
    params["gcmtype"] = "page|subcat"
    #---
    #print('<<lightblue>> API_CALLS %d  for %s' % (API_CALLS[1],enlink) )
    #----
    continue_p = ''
    continue_v = 'x'
    #---
    table = {}
    #----
    while continue_v != '' : 
        #---
        if continue_v != 'x':
            params[continue_p] = continue_v
        #---
        continue_v = ''
        #---
        api = mdwiki_api.post(params)
        #---
        if not api: break
        #---
        continue_d = api.get("continue", {})
        for p, v in continue_d.items():
            if p == 'continue' : continue
            continue_v = v
            continue_p = p
        #----
        pages = api.get( "query", {}).get( "pages", {})
        #----
        for category in pages:
            #---
            caca = category
            #---
            if type(pages) == dict: caca = pages[category]
            #---
            cate_title = caca["title"]
            tablese = {}
            #print("<<lightblue>> cate_title: %s" % cate_title ) 
            #---
            tablese['title'] = caca['title']
            #---
            if "ns" in caca:
                tablese['ns'] = caca['ns']
                #print("<<lightblue>> ns: %s" %  caca['ns']) 
            #---
            if 'templates' in caca:
                tablese['templates'] = [ x['title'] for x in caca['templates'] ]
            #---
            if 'langlinks' in caca:
                tablese['langlinks'] = {}
                for fo in caca['langlinks']:
                    result = fo['*']
                    tablese['langlinks'][fo['lang']] = fo['*']
            #---
            table[cate_title] = tablese
            #---
    #---
    return table
#---
def check_title(title):
    #---
    title = title.lower().strip()
    #---
    if title.find('(disambiguation)') != -1 :   return False
    if title.startswith('user:') :              return False
    #---
    return True
#---
def subcatquery( title, depth=0, ns="all", limit=0, test=False ): 
    #---
    # إيجاد categorymembers والتصانيف الفرعية لتصنيف
    #---
    #print('<<lightyellow>> catdepth.py sub cat query for %s:%s,depth:%d,ns:%s.' % ('',title,depth,ns) )
    #---
    start = time.time()
    final = time.time()
    #---
    if not title.strip().startswith('Category:') : title = 'Category:' + title.strip()
    #---
    tablemember = Get_cat( title, print_url = True )
    #---
    # result_table = { x : da for x, da in tablemember.items() if check_title(x) }
    result_table = { x : da for x, da in tablemember.items() if int(da["ns"]) == 0 }
    #---
    # for x in tablemember: if check_title(x) :  result_table[x] = tablemember[x]
    #---
    cat_done = []
    #---
    new_list = [ v['title'] for x, v in tablemember.items() if int(v["ns"]) == 14 ]
    #---
    if type(depth) != int and depth.isdigit():  depth = int(depth)
    #---
    if 'newlist' in sys.argv: print('lenof main cat:%d' % len(result_table) )
    #---
    depth_done = 0
    #--- 
    while depth > depth_done :#and ( limit > 0 and len(result_table) < limit ):
        depth_done += 1
        new_tab2 = []
        #---
        for cat in new_list:
            if not cat in cat_done:
                cat_done.append(cat)
                #---
                table2 = Get_cat(cat)
                #---
                for x, tabla in table2.items():
                    #---
                    if int(tabla["ns"]) == 14 or tabla["title"].startswith('Category:'):
                        new_tab2.append( x )
                    #---
                    if ns in [0,'0'] : 
                        if int(tabla["ns"]) == 0:
                            result_table[x] = tabla
                    else:
                        result_table[x] = tabla
        #---
        new_list = new_tab2
    #---
    final = time.time()
    delta = int(final - start)
    #---
    #if "printresult" in sys.argv: print(result_table)
    #---
    if 'newlist' in sys.argv:
        print('<<lightblue>>catdepth.py: find %d pages(ns:%s) in %s, depth:%d, subcat:%d in %d seconds' % (len(result_table), str(ns), title, depth,len(cat_done), delta ) )
        if len(cat_done) > 0 :
            print('subcats:%s' % ', '.join(cat_done))
    #---
    result_tab = list( result_table.keys() )
    #---
    #return result_table
    return result_tab
#---
def subcatquery2( cat, depth = 0, ns="all", limit=0 , test=False ): 
    filename = project + '/public_html/Translation_Dashboard/cats_cash/%s.json' % cat
    #---
    if cat == 'RTT' : depth = 2
    #---
    if not os.path.isfile(filename):
        #---
        try:
            with open( filename, 'w') as uu: json.dump({}, uu)
        except Exception as e:
            print( 'Traceback (most recent call last):' )
            print(f'<<lightred>> {__file__} Exception:' + str(e) )
            print( 'CRITICAL:' )
        #---
    #---
    try:
        textn = codecs.open( filename, "r", encoding="utf-8").read() 
    except Exception as e:
        print( 'Traceback (most recent call last):' )
        pywikibot.output(traceback.format_exc())
        print( 'CRITICAL:' )
        textn = ''
    #---
    Table = {}
    if textn != '' : Table = json.loads( textn )
    #---
    if str(Table.get('Day_History','')) != str(Day_History) or 'newlist' in sys.argv or len(Table['list']) < 1500 :
        #---
        if 'print' in sys.argv: print('get new catmembers')
        #---
        Listo = subcatquery( cat , depth = depth , ns = ns , limit = limit , test = test )
        Table = {}
        #---
        Table['list'] = [ x for x in Listo if check_title(x) ]
        #---
        Table['Day_History'] = Day_History
        #---
        json.dump(Table, open( filename , 'w'))
        #---
    #---
    if 'print' in sys.argv: print('len of list:%d' % len(Table['list']) )
    #---
    return Table
#---
def get_RTT():
    #---
    Listo = subcatquery( 'RTT', depth = '3', ns = '0' )
    #---
    # Listo = Listo['list']
    #---
    for x in Listo[:]:
        if x.startswith('Category:') :
            Listo.remove(x)
    #---
    return Listo
#---
all_pages = []
#---
def make_cash_to_cats(return_all_pages=False):
    #---
    cac = sql_for_mdwiki.mdwiki_sql('select category, depth from categories;', return_dict=True)
    #---
    cats = {}
    #---
    for c in cac:
        cat = c['category']
        dep = c['depth']
        #---
        cat = cat.decode("utf-8") if type(cat) == bytes else cat
        #---
        dep = dep.decode("utf-8") if type(dep) == bytes else dep
        #---
        cats[cat] = dep
    #---
    for cat, depth in cats.items():
        ca = subcatquery2( cat, depth=depth, ns='all' )
        #---
        print(f"len of pages in {cat}, depth:{depth}, : %d" % len(ca['list']) )
        #---
        for x in ca['list']:
            if not x in all_pages:
                all_pages.append(x)
    #---
    if return_all_pages:
        return all_pages
    #---
#---
if __name__ == '__main__':
    make_cash_to_cats()