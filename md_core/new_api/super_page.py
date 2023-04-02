from warnings import warn
import pywikibot
import urllib
import requests
import os
import json
import sys
import wikitextparser
#---
"""

from new_api.mdwiki_page import MainPage
'''
page      = MainPage(title, 'ar', family='wikipedia')
exists    = page.exists()
if not exists: return
#---
page_edit = page.can_edit()
if not page_edit: return
#---
if page.isRedirect() :  return
# target = page.get_redirect_target()
#---
text        = page.get_text()
ns          = page.namespace()
links       = page.page_links()
categories  = page.get_categories(with_hidden=False)
langlinks   = page.get_langlinks()
wiki_links  = page.get_wiki_links_from_text()
refs        = page.Get_tags(tag='ref')# for x in ref: name, contents = x.name, x.contents
words       = page.get_words()
templates   = page.get_templates()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
create      = page.Create(text='', summary='')
#---
back_links  = page.page_backlinks()
text_html   = page.get_text_html()
hidden_categories= page.get_hidden_categories()
flagged     = page.is_flagged()
timestamp   = page.get_timestamp()
user        = page.get_user()
purge       = page.purge()
'''

"""
#---
# from new_api import botEdit
from new_api import txtlib
from new_api import printe
# ingr = txtlib.extract_templates_and_params(text)
# for temp in ingr: name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
#---
print_test = {1:False}
#---
Edit_summary_line = { 1 : ' -Edit summary: %s:' }
#---
import inspect
def warn_err(err):
    err = str(err)
    nn = inspect.stack()[1][3]
    return f'\ndef {nn}(): {err}'
#---
Save_Edit_Pages = { 1 : False}
#---
change_codes = {
    "nb" : "no",
    "bat_smg" : "bat-smg",
    "be_x_old" : "be-tarask",
    "be-x-old" : "be-tarask",
    "cbk_zam" : "cbk-zam",
    "fiu_vro" : "fiu-vro",
    "map_bms" : "map-bms",
    "nds_nl" : "nds-nl",
    "roa_rup" : "roa-rup",
    "zh_classical" : "zh-classical",
    "zh_min_nan" : "zh-min-nan",
    "zh_yue" : "zh-yue",
    }
#---
def login_def(lang, family) :{}
#---
not_loged_m = {1:""}
#---
class MainPage():
    def __init__(self, title, lang, family='wikipedia'):
        self.title = title
        #---
        self.lang = change_codes.get(lang) or lang
        #---
        self.family = family
        self.endpoint = f'https://{lang}.{family}.org/w/api.php'
        #---
        self.username = ''
        self.Exists = ''
        self.is_redirect = ''
        self.flagged = ''
        self.can_be_edit = False
        #---
        self.wikibase_item = ""
        self.text = ""
        self.text_html = ""
        #---
        self.revid = ""
        self.newrevid = ""
        #---
        self.pageid = ""
        self.timestamp = ""
        self.user = ""
        #---
        self.back_links = []
        self.links = []
        self.iwlinks = []
        self.links_here = []
        #---
        self.info = {'done':False}
        #---
        self.categories = {}
        self.hidden_categories = {}
        self.all_categories_with_hidden = {}
        #---
        self.langlinks = {}
        self.templates = {}

        self.r3_token = ''
        self.summary = ''
        self.words = 0
        self.length = 0
        self.ns = False
        self.newtext = ""
        #---
        self.log = login_def(self.lang, family=self.family)
        #---
        if self.lang != "" and self.log.not_loged and self.lang != not_loged_m[1]:
            #---
            self.log.Log_to_wiki()
            #---
            not_loged_m[1] = self.lang
            #---
            self.r3_token = self.log.r3_token
            self.username = self.log.username
            #---
    #---
    def get_text(self, redirects=False):
        params = {
            "action": "query",
            "prop": "revisions|pageprops|flagged",
            "titles": self.title,
            "ppprop": "wikibase_item",              # pageprops
            "rvprop": "timestamp|content|user|ids", # revisions
            "rvslots": "*"                          # revisions
        }
        #---
        if redirects:    params["redirects"] = 1
        data = self.log.post(params)
        #---
        _dat_ = {"batchcomplete": "","query": {
                "normalized": [{"from": "وب:ملعب", "to": "ويكيبيديا:ملعب"}],
                "pages": {
                    "361534": {
                        "pageid": 361534,
                        "ns": 4,
                        "title": "ويكيبيديا:ملعب",
                        "revisions": [{
                            "revid": 61421668,
                            "parentid": 61421528,
                            "user": "Al-shazali Sabeel",
                            "timestamp": "2023-03-07T13:50:29Z",
                            "slots": {"main": {"contentmodel": "wikitext","contentformat": "text/x-wiki","*": "{{عنوان الملعب}}"}}
                        }],
                        "pageprops": {"wikibase_item": "Q3938" }
                    }
                }
        }}
        #---
        pages = data.get("query", {}).get("pages", {})
        #---
        for k, v in pages.items():
            #---
            if print_test[1] or 'printdata' in sys.argv: warn(warn_err('v:' + str(v)), UserWarning)
            #---
            if 'missing' in v :
                self.Exists = False
                break
            else:
                self.Exists = True
            #---
            title   = v["title"]
            #---
            pageprops = v.get("pageprops", {})
            self.wikibase_item   = pageprops.get("wikibase_item") or self.wikibase_item
            #---
            # "flagged": { "stable_revid": 61366100, "level": 0, "level_text": "stable"}
            self.flagged = v.get('flagged', False) != False
            #---
            self.ns      = v.get("ns") or self.ns
            self.pageid  = v.get("pageid") or self.pageid
            #---
            page = v.get("revisions", [{}])[0]
            #---
            self.text   = page.get("slots",{}).get("main",{}).get("*",'')
            self.user   = page.get("user")  or self.user
            self.revid  = page.get("revid") or self.revid
            #---
            self.timestamp = page.get("timestamp") or self.timestamp
            #---
            break
        #---
        return self.text

    def get_infos(self):
        #---
        params = {
            "action": "query",
            "titles": self.title,
            "prop": "categories|langlinks|templates|linkshere|iwlinks|info",
            "clprop": "sortkey|hidden",

            "cllimit": "max",       # categories
            "lllimit": "max",       # langlinks
            "tllimit": "max",       # templates
            "lhlimit": "max",       # linkshere
            "iwlimit": "max",       # iwlinks
            "formatversion": "2",
            # "normalize": 1,
            "tlnamespace": "10"
        }
        #---
        _data_ = {
            "continue": {},
            "query": {
                "pages": {
                    "9124097": {
                        "pageid": 9124097,
                        "ns": 0,
                        "title": "طواف العالم للدراجات 2023",
                        "categories": [],
                        "langlinks": [],
                        "templates": [{"ns": 10,"title": "قالب:-"}],
                        "linkshere": [{"pageid": 189150,"ns": 0,"title": "طواف فرنسا"}],
                        "iwlinks": [{"prefix": "commons","*": "Category:2023_UCI_World_Tour"}],
                        "contentmodel": "wikitext",
                        "pagelanguage": "ar",
                        "pagelanguagehtmlcode": "ar",
                        "pagelanguagedir": "rtl",
                        "touched": "2023-03-07T11:53:53Z",
                        "lastrevid": 61366100,
                        "length": 985
                    }
                }
            }
        }
        #---
        data = self.log.post(params)
        #---
        xs = {'batchcomplete': True, 'query': {'pages': [{'pageid': 151314, 'ns': 10, 'title': 'قالب:أوب',

        'categories': [
            {'ns': 14, 'title': 'تصنيف:قوالب تستخدم أنماط القوالب', 'sortkey': '', 'sortkeyprefix': '', 'hidden': False}, 
            {'ns': 14, 'title': 'تصنيف:cc', 'sortkey': 'v', 'sortkeyprefix': 'أوب', 'hidden': True}
            ],

        'langlinks': [{'lang': 'bh', 'title': 'टेम्पलेट:AWB'}], 

        'templates': [{'ns': 10, 'title': 'قالب:No redirect'}], 

        'linkshere': [{'pageid': 308641, 'ns': 10, 'title': 'قالب:AWB', 'redirect': True}], 

        'iwlinks': [{'prefix': 'd', 'title': 'Q4063270'}], 

        'contentmodel': 'wikitext', 'pagelanguage': 'ar', 'pagelanguagehtmlcode': 'ar', 'pagelanguagedir': 'rtl', 'touched': '2023-03-05T22:10:23Z', 'lastrevid': 61388266, 'length': 3477
        }
        ]}}
        #---
        ta = data.get("query", {}).get("pages", [{}])[0]
        #---
        #for _, ta in pages.items():
        #---
        self.ns     = ta.get('ns')        or self.ns
        self.pageid = ta.get('pageid')    or self.pageid
        self.length = ta.get('length')    or self.length
        self.revid  = ta.get('lastrevid') or self.revid
        #---
        self.is_redirect = True if 'redirect' in ta else False
        #---
        for cat in ta.get('categories', []):
            #---
            _cat_ = {"ns": 14,"title": "تصنيف:بوابة سباق الدراجات الهوائية/مقالات متعلقة","sortkey": "d8b7","sortkeyprefix": "","hidden": True  }
            #---
            if 'sortkey' in cat: del cat['sortkey']
            #---
            tit = cat["title"]
            #---
            self.all_categories_with_hidden[tit] = cat
            #---
            if cat.get('hidden') == True:
                self.hidden_categories[tit] = cat
            else:
                del cat['hidden']
                self.categories[tit] = cat
        #---
        if ta.get('langlinks', []) != []:
            #---
            # {"lang": "ca", "*": "UCI World Tour 2023"} or {'lang': 'bh', 'title': 'टेम्पलेट:AWB'}
            #---
            self.langlinks = { ta["lang"]: ta.get("*") or ta.get("title") for ta in ta.get('langlinks', []) }
        #---
        # "linkshere": [{"pageid": 189150,"ns": 0,"title": "طواف فرنسا"}, {"pageid": 308641,"ns": 10,"title": "قالب:AWB","redirect": ""}]
        self.links_here = ta.get('linkshere', [])
        #---
        self.iwlinks = ta.get('iwlinks', [])
        #---
        self.info['done'] = True

    def page_backlinks(self, ns=0):
        params = {
            "action": "query",
            "maxlag": "3",
            # "prop": "info",
            "generator": "backlinks",
            "redirects": 1,
            # 'gblfilterredir': 'redirects',
            "gbltitle":self.title,
            "gblnamespace": ns,
            "gbllimit": "max",
            "formatversion": "2",
            "gblredirect": 1
        }
        data = self.log.post(params)
        #---
        x = {
            'batchcomplete': True,
            'limits': {'backlinks': 2500},
            'query': {
                'redirects': [{'from': 'فريدريش زيمرمان','to': 'فريدريش تسيمرمان'}],
                'pages': [
                    {'pageid': 2941285,'ns': 0,'title': 'فولفغانغ شويبله'},
                    {'pageid': 4783977,'ns': 0,'title': 'وزارة الشؤون الرقمية والنقل'},
                    {'pageid': 5218323,'ns': 0,'title': 'فريدريش تسيمرمان'},
                    {'pageid': 6662649,'ns': 0,'title': 'غونتر كراوزه'}
                    ]
        }}
        #---
        pages = data.get("query", {}).get("pages", [])
        #---
        back_links = [ x for x in pages if x['title'] != self.title]
        #---
        self.back_links = back_links
        #---
        return self.back_links

    def page_links(self):
        params = {
            "action": "parse",
            "prop": "links",
            "formatversion": "2",
            "page": self.title
        }
        data = self.log.post(params)
        #---
        # [{'ns': 14, 'title': 'تصنيف:مقالات بحاجة لشريط بوابات', 'exists': True}, {'ns': 14, 'title': 'تصنيف:مقالات بحاجة لصندوق معلومات', 'exists': False}]
        #---
        self.links = data.get('parse', {}).get('links', [])
        #---
        return self.links

    def get_text_html(self):
        params = {
            "action": "parse",
            "page": self.title,
            "formatversion": "2",
            "prop": "text"
        }
        #---
        data = self.log.post(params)
        #---
        _data_ = {'warnings': {'main': {'warnings': 'Unrecognized parameter: bot.'}}, 'parse': {'title': 'ويكيبيديا:ملعب', 'pageid': 361534, 'text': ''}}
        #---
        self.text_html = data.get('parse', {}).get('text', '')
        #---
        return self.text_html

    def get_redirect_target(self):
        #---
        params = {
            "action": "query",
            "titles": self.title,
            "prop": "info",
            "redirects": 1
        }
        #---
        data = self.log.post(params)
        #---
        _pages_ = {'batchcomplete': '', 'query': {'redirects': [{'from': 'Yemen', 'to': 'اليمن'}], 'pages': {}, 'normalized': [{'from': 'yemen', 'to': 'Yemen'}] }}
        #---
        __redirects__ = {'from': 'Yemen', 'to': 'اليمن'}
        #---
        redirects = data.get("query", {}).get("redirects", [{}])[0]
        #---
        to = redirects.get("to", '')
        #---
        if to != '' :
            printe.output(f'<<lightyellow>>Page:{self.title} redirect to {to}')
        #---
        return to

    def get_words(self):
        srlimit = "30"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": self.title,
            "srlimit": srlimit,
        }
        data = self.log.post(params, addtoken = True)
        #---
        if data == {}: return 0
        #---
        search = data.get('query', {}).get('search', [])
        #---
        for pag in search:
            tit = pag["title"]
            count = pag["wordcount"]
            if tit == self.title:
                self.words = count
                break
        #---
        return self.words

    def purge(self):
        #---
        params = {
            "action": "purge",
            "forcelinkupdate": 1,
            "forcerecursivelinkupdate": 1,
            "titles": self.title
        }
        #---
        data = self.log.post(params, Type='post')
        #---
        if data == {}:
            printe.output('<<lightred>> ** purge error. ')
            return False
        #---
        title2 = self.title
        #---
        #  'normalized': [{'from': 'وب:ملعب', 'to': 'ويكيبيديا:ملعب'}]}
        #---
        for x in data.get('normalized', []):
            # printe.output(f"normalized from {x['from']} to {x['to']}")
            if x['from'] == self.title :
                title2 = x['to']
                break
        #---
        for t in data.get('purge', []):
            # t = [{'ns': 4, 'title': 'ويكيبيديا:ملعب', 'purged': '', 'linkupdate': ''}]
            ti = t['title']
            if title2 == ti and 'purged' in t:
                return True
            if "missing" in t:
                printe.output( 'page "%s" missing' % t['title'] )
                return "missing"
        return False

    def isRedirect(self):
        #---
        if self.is_redirect == '': self.get_infos()
        #---
        return self.is_redirect
    #---
    def get_categories(self, with_hidden=False):
        #---
        # if self.categories == {}: self.get_infos()
        if not self.info['done']: self.get_infos()
        #---
        if with_hidden:
            return self.all_categories_with_hidden
        #---
        return self.categories

    def get_hidden_categories(self):
        #---
        if self.categories == {} and self.hidden_categories == {} : self.get_infos()
        #---
        return self.hidden_categories

    def get_langlinks(self):
        #---
        if not self.info['done']: self.get_infos()
        #---
        return self.langlinks

    def get_links_here(self):
        #---
        if not self.info['done']: self.get_infos()
        #---
        return self.links_here

    def get_wiki_links_from_text(self):
        if self.text == '' : self.text = self.get_text()
        #---        
        parsed = wikitextparser.parse(self.text)
        wikilinks = parsed.wikilinks
        #---
        printe.output(f'wikilinks:{str(wikilinks)}')
        #---
        for x in wikilinks:
            print(x.title)
        #---
        return self.can_be_edit

    def Get_tags(self, tag=''):
        if self.text == '' : self.text = self.get_text()
        #---
        self.text = self.text.replace('<ref>', '<ref name="ss">', 1)
        #---
        parsed = wikitextparser.parse(self.text)
        tags = parsed.get_tags()
        #---
        # printe.output(f'tags:{str(tags)}')
        #---
        if tag == '':
            return tags
        #---
        new_tags = []
        #---
        for x in tags:
            if x.name == tag:
                new_tags.append(x)
        #---
        return new_tags

    def can_edit(self, script=''):
        if self.text == '' : self.text = self.get_text()
        #---
        self.can_be_edit = True#botEdit.botMayEdit( False, text= self.text, title_page=self.title, botjob=script)
        #---
        return self.can_be_edit

    def is_flagged(self):
        #---
        if self.text == '' : self.text = self.get_text()
        #---
        return self.flagged

    def get_timestamp(self):
        if self.timestamp == '' : self.get_text()
        return self.timestamp

    def exists(self):
        if self.Exists == '' : self.get_text()
        if not self.Exists:
            printe.output( f'page "{self.title}" not exists' )
        return self.Exists

    def namespace(self):
        if self.ns == False : self.get_text()
        return self.ns

    def get_user(self):
        if self.user == '' : self.get_text()
        return self.user

    def get_templates(self):
        if self.text == '' : self.text = self.get_text()
        self.templates = txtlib.extract_templates_and_params(self.text)
        return self.templates

    def ask_put(self, nodiff = False):
        yes_answer = [ "y", "a", "", "Y", "A", "all", "aaa" ]
        #---
        if 'ask' in sys.argv and not Save_Edit_Pages[1] or print_test[1]:
            #---
            if not "nodiff" in sys.argv and not nodiff:
                printe.showDiff(self.text, self.newtext)
            #---
            printe.output(Edit_summary_line[1] % self.summary )
            sa = pywikibot.input('<<lightyellow>>page.py: Do you want to accept these changes? (yes, no): for page %s:%s user:%s'  % (self.lang, self.title, self.username ))
            #---
            if sa == "a":
                printe.output('<<lightgreen>> ---------------------------------' )
                printe.output(f'<<lightgreen>> {__file__} save all without asking.' )
                printe.output('<<lightgreen>> ---------------------------------' )
                Save_Edit_Pages[1] = True
            #---
            if not sa in yes_answer:
                printe.output( "wrong answer" )
                return False
        #---
        return True

    def handel_err(self, error, function):
        #---
        # {'error': {'code': 'articleexists', 'info': 'The article you tried to create has been created already.', '*': 'See https://ar.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1425'}
        #---
        err_code = error.get('code', '')
        err_info = error.get('info', '')
        #---
        tt = f'<<lightred>>{function} ERROR: <<defaut>>code:{err_code}.'
        # printe.output(tt)
        warn(warn_err(tt), UserWarning)
        #---["protectedpage", 'تأخير البوتات 3 ساعات', False]
        if err_code == "abusefilter-disallowed":
            #---
            # oioioi = {'error': {'code': 'abusefilter-disallowed', 'info': 'This', 'abusefilter': {'id': '169', 'description': 'تأخير البوتات 3 ساعات', 'actions': ['disallow']}, '*': 'See https'}, 'servedby': 'mw1374'}
            #---
            abusefilter = error.get("abusefilter","")
            description = abusefilter.get('description','')
            printe.output('<<lightred>> ** abusefilter-disallowed: %s ' % description )
            if description == 'تأخير البوتات 3 ساعات' :
                return False
            return description
        #---
        if err_code == "protectedpage":
            printe.output('<<lightred>> ** protectedpage. ')
            # return "protectedpage"
            return False
        #---
        if err_code == "articleexists":
            printe.output('<<lightred>> ** article already created. ')
            return "articleexists"
        #---
        printe.output(f'<<lightred>>{function} ERROR: <<defaut>>info: {err_info}.')

    def save(self, newtext='', summary='', nocreate=1, minor='', tags='', nodiff=False):
        #---
        self.newtext = newtext
        if summary != '':
            self.summary = summary
        #---
        ask = self.ask_put(nodiff=nodiff)
        if ask == False : return False
        #---
        params = {
            "action": "edit",
            "title": self.title,
            "text": newtext,
            "summary": self.summary,
            "minor": minor,
            "nocreate": nocreate,
        }
        #---
        if self.revid != '' : params['baserevid'] = self.revid
        #---
        if tags != "" :params["tags"] = tags
        #---
        # params['basetimestamp'] = self.timestamp
        #---
        pop = self.log.post(params, addtoken=True)
        #---
        if pop == {}: return False
        #---
        error  = pop.get('error',{})
        edit   = pop.get('edit',{})
        result = edit.get('result','')
        #---
        # {'edit': {'result': 'Success', 'pageid': 5013, 'title': 'User:Mr. Ibrahem/sandbox', 'contentmodel': 'wikitext', 'oldrevid': 1336986, 'newrevid': 1343447, 'newtimestamp': '2023-04-01T23:14:07Z', 'watched': ''}}
        #---
        if result.lower() == 'success':
            self.text = newtext
            self.user = ''
            printe.output('<<lightgreen>> ** true .. ' + '[[%s:%s:%s]] ' % (self.lang, self.family, self.title)  )
            printe.output( 'تم بنجاح... time.sleep() ')
            #---
            if 'printpop' in sys.argv:
                print(pop)
            #---
            self.pageid = edit.get('pageid')   or self.pageid
            self.revid  = edit.get('newrevid') or self.revid
            self.newrevid  = edit.get('newrevid') or self.newrevid
            self.timestamp = edit.get('newtimestamp') or self.timestamp
            #---
            return True
        #---
        if error != {}:
            er = self.handel_err(error, function='Save')
            #---
            return er
        #---
        return False

    def Create(self, text='', summary=''):
        #---
        self.newtext = text
        #---
        ask = self.ask_put()
        #---
        if ask == False : return False
        #---
        params = {
            "action": "edit",
            "title": self.title,
            "text": text,
            "summary": summary,
            "notminor": 1,
            "createonly": 1,
        }
        #---
        pop = self.log.post(params, addtoken=True)
        #---
        if pop == {}: return False
        #---
        error  = pop.get('error',{})
        edit   = pop.get('edit',{})
        result = edit.get('result','')
        #---
        if print_test[1] :
            print('pop:')
            print(pop)
        #---
        if result.lower() == 'success':
            #---
            #{'edit': {'new': '', 'result': 'Success', 'pageid': 9090918, 'title': 'مستخدم:Mr. Ibrahem/test2024', 'contentmodel': 'wikitext', 'oldrevid': 0, 'newrevid': 61016221, 'newtimestamp': '2023-02-01T21:52:42Z'}}
            #---
            self.text = text
            #---
            printe.output('<<lightgreen>> ** true .. ' + '[[%s:%s:%s]] ' % (self.lang, self.family, self.title)  )
            printe.output( 'تم بنجاح... time.sleep() ')
            #---
            self.pageid = edit.get('pageid')   or self.pageid
            self.revid  = edit.get('newrevid') or self.revid
            self.newrevid  = edit.get('newrevid') or self.newrevid
            self.timestamp = edit.get('newtimestamp') or self.timestamp
            #---
            return True
        #---
        if error != {}:
            er = self.handel_err(error, function='Create')
            #---
            return er
            #---
        return False
#---