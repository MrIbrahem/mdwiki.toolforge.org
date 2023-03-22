'''

write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]
'''
import sys
from collections import namedtuple
import os
import re
import json
import urllib.parse
import requests
import wikitextparser
import codecs
from mdpy import mdwiki_api
from mdpy import printe
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project += '/md_core/prior/'
#---
def main_links():
    title = "WikiProjectMed:List/Prior"
    text  = mdwiki_api.GetPageText(title)
    links = mdwiki_api.Get_page_links(title, namespace="*", limit="max")
    # print(links)
    #---
    links = [ x['title'] for s, x in links['links'].items() if x['ns'] == 0 ]
    #---
    # log all links to file
    codecs.open(project + 'links.json', 'w', encoding='utf-8').write(json.dumps(links))
    #---
    printe.output(f'{len(links)} links found')
    #---
    return links
#---
from newapi.page import MainPage
#---
def print_test(s):
    if 'test' in sys.argv:print(s)
#---
def get_weblinks(refs, text):
    liste = []
    #---
    if text != '':
        weblinks = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        # add to list
        liste.extend(weblinks)
    #---
    else:
        for x in refs:
            '''x like:
            <ref>{{cite web
            |url=https://bbc.com
            |title=BBC
            }}
            '''
            name, contents = x.name, x.contents
            # match weblinks in contents like http using regex
            weblinks = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', contents)
            # add to list
            liste.extend(weblinks)
    #---
    liste1 = []
    # delete link like web.archive.org
    for x in liste:
        if 'web.archive.org' in x: continue
        #---
        x = x.replace('//www.', '//').replace('http://', 'https://')
        #---
        # un urlencode 
        # x = x.replace('%3A', ':').replace('%2F', '/').replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
        x = urllib.parse.unquote(x)
        #---
        liste1.append(x)
    #---
    # remove duplicates
    liste1 = list(set(liste1))
    #---
    return liste1
#---
if not os.path.exists(project + 'allen.json'):
    codecs.open(project + 'allen.json', 'w', encoding='utf-8').write(json.dumps({}))
#---
all = json.loads(codecs.open(project + 'allen.json', 'r', encoding='utf-8').read())
#---
def work_in_one_lang_link(lang, title):
    #---
    params = { "action": "parse", "format": "json", "prop": "wikitext", "page": title, "utf8": 1}
    #---
    json1 = {}
    #---
    try:
        session = requests.Session()
        req = session.post('https://' +  lang + '.wikipedia.org/w/api.php', data=params)
        json1 = req.json()
    except Exception as e:
        printe.output(f'except: {e}')
    #---
    text = json1.get('parse',{}).get('wikitext',{}).get('*','')
    #---
    parsed = wikitextparser.parse(text)
    tags = parsed.get_tags()
    #---
    refs = []
    #---
    for x in tags:
        if x.name == 'ref': refs.append(x)
    #---
    weblinks = get_weblinks(refs, text)
    #---
    return weblinks
#---
def work_in_en_page(title):
    #---
    if not title in all : all[title] = {'refs':0, 'langs':{}}
    #---
    page	  = MainPage(title, 'en')
    exists	  = page.exists()
    #---
    text = page.get_text()
    #---
    if not exists: return
    #---
    refs    = page.Get_tags(tag='ref')
    en_weblinks = get_weblinks(refs, text)
    printe.output(f'{len(en_weblinks)} en refs found')
    #---
    print_test("\n*".join(en_weblinks))
    #---
    all[title]['refs'] = len(en_weblinks)
    #---
    if len(en_weblinks) == 0: return
    #---
    langlinks = page.get_langlinks()
    #---
    print_test(f"langlinks: {len(langlinks)}")
    #---
    n = 0
    #---
    for lang, tit in langlinks.items():
        # printe.output(f'{lang}: {tit}')
        #---
        n += 1
        #---
        web_links = work_in_one_lang_link(lang, tit)
        #---
        if len(web_links) == 0: continue
        #---
        same = [ x for x in web_links if x in en_weblinks ]
        #---
        printe.output(f'p{n}/{len(langlinks)}:\t{lang}\t{len(web_links)} refs, {len(same)} same')
        #---
        if len(same) == 0: continue
        #---
        all[title]['langs'][lang] = {'title':tit, 'refs': len(web_links), 'same': len(same) }
        #---
    #---
    codecs.open(project + 'allen.json', 'w', encoding='utf-8').write(json.dumps(all, indent=4))
#---
def start():
    #---
    if 'test' in sys.argv:
        links = ['Abacavir']
    else:
        links = main_links()
    #---
    # start work in all links
    for x in links:
        work_in_en_page(x)
#---
class testmycode(object):
    def __init__(self):
        self.test_incomplete_links()
    # Tests that input list contains references with incomplete web links and the function returns a list of extracted web links with complete urls. tags: [edge case]
    def test_incomplete_links(self):
        a = namedtuple('a', ['name', 'contents'])
        a.name = 'a'
        a.contents = '<ref>{{cite web |url=https://www.bbc.com |title=BBC}}</ref>'
        b = namedtuple('b', ['name', 'contents'])
        b.name = 'b'
        b.contents = '<ref>{{cite web |url=https://www.cnn.com |title=CNN}}</ref>'
        refs = [a, b]
        expected = ['https://www.bbc.com', 'https://www.cnn.com']
        f = get_weblinks(refs, '')
        print(f)
        print('test_incomplete_links: ' + str(set(f) == set(expected)))
#---
if __name__ == '__main__':
    if 'test2' in sys.argv:
        testmycode()
    else:
        start()