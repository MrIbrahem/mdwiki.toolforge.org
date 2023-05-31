"""

from priorviews.links_by_section import sects_links_langlinks

python3 ./core8/pwb.py priorviews/links_by_section

"""
import sys
import pywikibot
import json
import os
import codecs
from mdpy import printe
#---
from priorviews.sections_links import get_section_links
#---
Dir = os.path.dirname(os.path.abspath(__file__))
_Dir_ = os.path.dirname(Dir)
file = f'{_Dir_}/prior/all_pages_states.json'
#---
data = json.load(codecs.open(file, 'r', 'utf-8'))
#---
printe.output(f'<<lightgreen>> len of data: {len(data)}')
#---
mdtitles_lang_title = {}
#---
for mdtitle, langs in data.items():
    #---
    newlangs = {lang: v['title'] for lang, v in langs.items() if v['title'] != '' and v['color'] == 'green'}
    #---
    # if 'test' in sys.argv: print(newlangs)
    #---
    mdtitles_lang_title[mdtitle] = newlangs
#---
printe.output(f'<<lightgreen>> len of mdtitles_lang_title: {len(mdtitles_lang_title)}')
#---
sections_links = get_section_links()
#---
sects_links_langlinks = {}
#---
links_done = []
#---
# split lists by sections
for section, links in sections_links.items():
    #---
    _links_ = ['Tooth decay', 'Angular cheilitis', 'Bad breath', 'Leukoplakia', 'Periodontal disease', 'Tonsil stones']
    #---
    sec_links = {x: tab for x, tab in mdtitles_lang_title.items() if x in links}
    #---
    links_done.extend(sec_links.keys())
    #---
    sects_links_langlinks[section] = sec_links
#---
printe.output(f'<<lightgreen>> len of sects_links_langlinks: {len(sects_links_langlinks)}')
#---
links_done = list(set(links_done))
#---
if len(links_done) != len(mdtitles_lang_title.keys()):
    print(f'len of links_done: {len(links_done)}')
    #---
    # find diff
    #---
    diff = list(set(mdtitles_lang_title.keys()) - set(links_done))
    #---
    printe.output(f'<<lightred>> len of diff: {len(diff)}')
    print(diff)
#---
# find the section with the least links
least_section = min(sects_links_langlinks, key=lambda x: len(sects_links_langlinks[x]))
print(f'least section: {least_section}')
# print lenth of least_section in sects_links_langlinks
print(f'lenth of least_section: {len(sects_links_langlinks[least_section])}')
#---
sects_links_langlinks = sects_links_langlinks.copy()
#---
if 'test' in sys.argv:
    sects_links_langlinks = { least_section : sects_links_langlinks[least_section] }
#---
#---
if __name__ == '__main__':
    ll = sects_links_langlinks
    #---
    for s, ls in ll.items():
        print(f'section: {s}')
        print(f'len of links: {len(ls)}')
        if len(ls) < 10:
            print(ls)
