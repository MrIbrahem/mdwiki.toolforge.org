#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
python3 pwb.py nccommons/mv
"""
#
# (C) Ibrahem Qasim, 2023
#
#---
import re
import sys
import json
import time
import os
import codecs
import pywikibot
#---
project = "/mnt/nfs/labstore-secondary-tools-project/mdwiki"
#---
if not os.path.isdir(project):  project = "I:/mdwiki"
#---
from mdpy import mdwiki_api
#---
cats = json.load(codecs.open(f'{project}/md_core/nccommons/mv.json', 'r', 'utf-8'))
#---
pywikibot.output(f'len of cats: {len(cats)}')
#---
from nccommons import api
#---
from new_api.mdwiki_page import NEW_API
api_new = NEW_API('www', family='mdwiki')
# login   = api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
#---
exists = {}
# exists = api_new.Find_pages_exists_or_not(cats)
#---
to_create = [ x for x, t in exists.items() if t == False ]
#---
pywikibot.output(f'len of to_create: {len(to_create)}')
#---
n = 0
#---
for cat in to_create:
    n += 1
    pywikibot.output(f'cat: {n}/{len(to_create)}:')
    text = mdwiki_api.GetPageText(cat)
    new = api.create_Page(text, cat, summary='Copy categories from mdwiki')
#---
to_update = [ x for x, t in exists.items() if t == True ]
to_update = cats
#---
from new_api.ncc_page import MainPage as ncc_MainPage
#---
n = 0
#---
def delete_it(cat):
    #---
    pywikibot.output(f'cat: {n}/{len(to_update)}:')
    #---
    params = {"action": "delete","format": "json","title": cat, "reason": "cat moved to nccommons.org"}#, "deletetalk": 1}
    #---
    doit = mdwiki_api.post(params, addtoken=True)
    #---
    pywikibot.output(f'doit: {doit}')
#---
for cat in to_update:
    #---
    n += 1
    #---
    pywikibot.output(f'cat: {n}/{len(to_update)}:')
    #---
    nspage = ncc_MainPage(cat, 'www', family='nccommons')
    #---
    pywikibot.output(f'GetPageText for page:{cat}')
    #---
    md_text = mdwiki_api.GetPageText(cat)
    #---
    if md_text == '': continue
    #---
    nc_text = nspage.get_text()
    #---
    if md_text == nc_text:
        pywikibot.output(f'{cat} is up to date')
    else:
        save_page = nspage.save(newtext=md_text, summary='Copy from mdwiki', nocreate=1)
    #---
    delete_it(cat)
    #---
    if 'break' in sys.argv: break
    #---