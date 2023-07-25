'''
#---
from priorviews.lists import creators 
# creators.Creators_by_lang_title
# creators.counts_creators_by_lang
#---
python3 pwb.py priorviews/lists/creators

'''
import sys
import pywikibot
import json
import os
import re
import codecs
#---
Dir = os.path.dirname(os.path.abspath(__file__))
Dir2 = os.path.dirname(Dir)
#---
file = f'{Dir2}/lists/creators_by_lang.json'
#---
if not os.path.exists(file):
    with open(file, 'w') as f:  json.dump({}, f)
#---
CreatorsData = json.load(codecs.open(file, 'r', 'utf-8'))
#---
Creators_by_lang_title = {}
#---
counts_creators_by_lang  = {}
#---
# Iterate through each markdown file and language in `CreatorsData`
for lang, titles in CreatorsData.items():
    #---
    if not lang in counts_creators_by_lang: counts_creators_by_lang[lang] = {}
    if not lang in Creators_by_lang_title: Creators_by_lang_title[lang] = {}
    #---
    for title, tab in titles.items():
        #---
        actor  = tab["actor"]
        _time_ = tab["time"]
        TD     = tab["TD"]
        #---
        # if actor match IP address : skip
        if re.match(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", actor): continue
        # ---
        if not actor in counts_creators_by_lang[lang] : counts_creators_by_lang[lang][actor] = 0
        counts_creators_by_lang[lang][actor] += 1
        #---
        Creators_by_lang_title[lang][title] = tab
        #---
#---
if __name__ == '__main__':
    print(f'len of Creators_by_lang_title: {len(Creators_by_lang_title)}')
    for lang, titles in Creators_by_lang_title.items():
        for title, words in titles.items():
            print(lang, title, words)

    for x, wo in counts_creators_by_lang.items():
        print(x)
        for x, z in wo.items():
            print(x, z)
    #---
    print(f'len of counts_creators_by_lang: {len(counts_creators_by_lang)}')
    #---

#---