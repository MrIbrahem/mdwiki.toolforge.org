#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

إنشاء قائمة بالاهمية من الانجليزية

python pwb.py mdwiki/public_html/Translation_Dashboard/getas

python3 pwb.py /data/project/mdwiki/py/getas

python3 pwb.py py/getas newpages


"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import codecs
import os
import sys
sys_argv = sys.argv or []
import pywikibot
import catdepth2
#---
#---
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
pywikibot.output('Get vaild_links from cat : RTT' )
#---
tabe = catdepth2.subcatquery2( 'RTT', depth = '2', ns = '0' )
vaild_links = tabe['list']
#---
pywikibot.output('len of vaild_links: %d' % len(vaild_links) )
#---
json_file = { 0 : '' }
json_file[0] = project + '/public_html/Translation_Dashboard/Tables/assessments.json'
#---
old_assessments = {}
lala = ''
#---
with codecs.open( json_file[0] , "r", encoding="utf-8-sig") as listt:
    lala = listt.read()
listt.close()
#---
pywikibot.output( 'file_name:%s' % json_file[0] )
fa = str(lala)
if fa != '' : old_assessments = json.loads(fa)
#---
len_old = len(old_assessments)
#---
assessments = { x : z for x, z in old_assessments.items() }
#---
if 'newpages' in sys_argv:#vaild_links
    vaild_links2 = vaild_links
    vaild_links = [ xp for xp in vaild_links2 if (not xp in old_assessments or old_assessments.get(xp) in ["Unknown",""]) ]
    #---
    pywikibot.output( 'Category-members:%d,New-members:%d' % ( len(vaild_links2) , len(vaild_links) ) )
    #--- 
#---
Nore = { 1 : False }
for arg in sys_argv:
    if arg in [ 'new' , 'listnew' , 'less100' , 'more400' ] :
        Nore[1] = True
#--- 
#---
import wdapi
# wdapi.submitAPI( params , apiurl = 'https://' + 'www.wikidata.org/w/api.php' , returnjson = False )
# wdapi.submitAPI_token( params , apiurl = 'https://' + 'www.wikidata.org/w/api.php' , returnjson = False )
# wdapi.Getpageassessments_from_wikipedia( titlel, site="en", find_redirects=False, pasubprojects=0 )
#---
#---
def split_list_to_numbers( lll ):
    List = {}
    DDone = []
    num = 1
    #---
    for cc in lll:
        #---
        if not num in List: List[num] = []
        #---
        if len(List[num]) < 150 :
            if not cc in DDone:
                List[num].append( cc )
                DDone.append( cc )
                #---
                if len(List[num]) > 149 : num += 1
                #---
    #---
    return List   
#---
from en_to_md import *#mdwiki_to_enwiki#enwiki_to_mdwiki
#---
def log():
    with open( json_file[0] , 'w') as outfile:
        json.dump( assessments, outfile, sort_keys = True )
    outfile.close()
    #---
    pywikibot.output('<<lightgreen>> %d lines to %s' % ( len(assessments) , json_file[0] ) )
    pywikibot.output('<<lightgreen>> len old assessments %d' % len_old )
#---
def work_for_list(list):
    #---
    # من ميد إلى الإنجليزية
    listo = [ mdwiki_to_enwiki.get(cc,cc) for cc in list ]
    #---
    ase = wdapi.Getpageassessments_from_wikipedia("|".join(list), site='en')
    #---
    lenn = 0
    #---
    for title in ase:
        #---
        #{'pageid': 3186837, 'ns': 0, 'title': 'WAGR syndrome', 'pageassessments': {'Medicine': {'class': 'Start', 'importance': 'Low'}}}
        tabe = ase[title]
        #---
        importance = tabe.get('pageassessments',{}).get('Medicine',{}).get('importance','')
        #---
        # من الإنجليزية إلى ميد
        title = enwiki_to_mdwiki.get( title , title )
        #---
        lenn += 1
        #---
        assessments[title] = importance
    #---
    print(f'len of new assessments:{lenn}')
    #---
#---
def mmain():
    numb = 0
    #---
    kkk = { 1 : vaild_links }
    #---
    if not 'new' in sys_argv:
        #kkk = [ x for x in vaild_links if not x in old_assessments ]
        kkk[1] = []
        for x in vaild_links :
            x2 = x[0].upper() + x[1:]
            #if not x in old_assessments or 'listnew' in sys_argv:
            kkk[1].append( x2 )
    #---
    ll = split_list_to_numbers(kkk[1])
    #---
    for lis in ll:
        #---
        liste = ll[lis]
        #---
        work_for_list(liste)
        #---
        #log()
        #---
    #---
    log()
    #---
#---
if __name__ == '__main__':
    mmain()
#---
