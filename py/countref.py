#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

إنشاء قائمة بعدد المراجع

python3 pwb.py /data/project/mdwiki/py/countref less100

python3 pwb.py py/countref newpages

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import codecs
import re
import os
import sys
#---
sys_argv = sys.argv or []
#---
print_pywikibot = { 1 : False }
try:
    import pywikibot
    print_pywikibot[1] = True
except:
    print_pywikibot[1] = False
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
if not os.path.isdir(project): project = '/mdwiki'
#---
# start of mdwiki_api.py file
import mdwiki_api




















#---
all_ref = {}
lead_ref = {}
vaild_links = { 1 : [] }
list_ma = { 1 : [] }
#---
file_all  = project + '/public_html/Translation_Dashboard/Tables/all_refcount.json'
file_lead = project + '/public_html/Translation_Dashboard/Tables/lead_refcount.json'
#---
import catdepth2
#---
def Decode_bytes(x):
    if type(x) == bytes:
        x = x.decode("utf-8")
    return x
#---
a = {}
#---
a = json.loads(codecs.open(file_all, "r", encoding="utf-8").read())
#---
all_ref = { x : ref for x, ref in a.items() if ref > 0 }
#---
la = {}
#---
la = json.loads(codecs.open(file_lead, "r", encoding="utf-8").read())
#---
lead_ref = { x : ref for x, ref in la.items() if ref> 0 }
#---
# list for titles in both all_ref and lead_ref
list_fu = list( set(all_ref.keys()) & set(lead_ref.keys()) )
#---
# remove duplicates from list
list_fu = list(set(list_fu))
list_ma[1] = [ x for x in list_fu if (x in all_ref and x in lead_ref) ]
#---
def count_ref_from_text( text, get_short = False ):
    #---
    short_ref = re.compile( r'<ref\s*name\s*\=\s*(?P<name>[^>]*)\s*\/\s*>', re.IGNORECASE | re.DOTALL)
    #---
    ref_list = []
    #---
    # count = 0
    #---
    if get_short:
        for m in short_ref.finditer(text):
            name = m.group('name')
            if name.strip() != '' : 
                if not name.strip() in ref_list : ref_list.append(name.strip())
    #---      
    # refreg = re.compile(r'(<ref[^>]*>[^<>]+</ref>|<ref[^>]*\/\s*>)')
    refreg = re.compile( r'(?i)<ref(?P<name>[^>/]*)>(?P<content>.*?)</ref>', re.IGNORECASE | re.DOTALL)
    #---      
    for m in refreg.finditer(text):
        # content = m.group('content')
        # if content.strip() != '' : if not content.strip() in ref_list : ref_list.append(content.strip())
        #---
        name    = m.group('name')
        content = m.group('content')
        #---
        if name.strip() != '' :
            if not name.strip() in ref_list : ref_list.append(name.strip())
        elif content.strip() != '' :
            if not content.strip() in ref_list : ref_list.append(content.strip())
            # count += 1
    #---      
    count = len(ref_list)
    #---      
    return count
#---
from TDpynew import ref
# ref.fix_ref( first, alltext )
#---
def count_refs( title ):
    #---
    text = mdwiki_api.GetPageText(title)
    #---
    text2 = ref.fix_ref( text, text )
    #---
    all_c = count_ref_from_text( text2 )
    all_ref[title] = all_c
    #---
    leadtext = text2.split('==')[0]
    lead_c = count_ref_from_text( leadtext, get_short = True )
    #---
    lead_ref[title] = lead_c
    #---
    pywikibot.output('<<lightgreen>> all:%d \t lead:%d' % ( all_c, lead_c ) )
#---
def logaa(file,table):
    with open( file, 'w') as outfile:
        json.dump( table, outfile, sort_keys = True, indent=4)
    outfile.close()
    #---
    pywikibot.output('<<lightgreen>> %d lines to %s' % ( len(table), file ) )
#---
def from_sql():
    #---
    que = '''select title, word from pages;'''
    #---
    sq = sql_for_mdwiki.mdwiki_sql(que)
    #---
    titles2 = []
    #---
    for tab in sq :
        title  = Decode_bytes(tab[0])
        titles2.append(title)
        #---
    #---
    titles = [ x for x in titles2 if not x in list_ma[1] ]
    #---
    pywikibot.output( '<<lightyellow>> sql: find %d titles, %d to work. ' % (len(titles2), len(titles)) )
    return titles
#---
def get_links():
    tabe = catdepth2.subcatquery2( 'RTT', depth = '1', ns = '0' )
    lale = tabe['list']
    #---
    if 'sql' in sys.argv:
        lale = from_sql()
    #---
    if 'newpages' in sys_argv:
        lale = [ x for x in lale if ( not x in list_ma[1] )]
    #---
    return lale
#---
def mai():
    #---
    numb = 0
    #---
    vaild_links[1] = get_links()
    #---
    limit = 10000
    if 'limit100' in sys.argv : limit = 100
    #---
    # python pwb.py mdwiki/public_html/Translation_Dashboard/countref test1 local -title:Testosterone_\(medication\)
    # python3 pwb.py /data/project/mdwiki/py/countref test1 -title:Testosterone_\(medication\)
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(':')
        #---
        if arg == "-title" : vaild_links[1].append( value.replace('_',' ') )
        #---
    #---
    for x in vaild_links[1]:
        #---
        numb += 1
        #---
        if numb >= limit :  break
        #---
        pywikibot.output(' p %d from %d: for %s:' % (numb, len(vaild_links[1]), x) )
        #---
        count_refs(x)
        #---
        if numb == 10 or str(numb).endswith('00'):
            logaa(file_lead, lead_ref)
            logaa(file_all, all_ref)
        #---
    #---
    logaa(file_lead, lead_ref)
    logaa(file_all, all_ref)
#---
if __name__ == '__main__':
    mai()
#---
