'''

#---
from priorviews import views
#---
# views.views_by_mdtitle_langs
# views.count_views_by_mdtitle
# views.count_views_by_lang
# views.views_by_lang
#---

python3 ./core8/pwb.py priorviews/views

'''
import sys
import pywikibot
import json
import os
import re
import codecs
#---
Dir = os.path.dirname(os.path.abspath(__file__))
#---
file = f'{Dir}/views_mdwiki_langs.json'
#---
if not os.path.exists(file):
    with open(file, 'w') as f:  json.dump({}, f)
#---
ViewsData = json.load(codecs.open(file, 'r', 'utf-8'))
#---
_data = { 
    "mdtitle" : {
        "ar" : {"title": "artitle", "views" : 0},
        "en" : {"title": "entitle", "views" : 0}
    }
}
#---
views_by_mdtitle_langs = {}
count_views_by_mdtitle = {}
#---
count_views_by_lang  = {}
views_by_lang        = {}
#---
def makeviews():
    #---
    """
    This function iterates through the `_data_` dictionary and updates the
    `count_views_by_mdtitle`, `count_views_by_lang`, and `views_by_lang`
    dictionaries with the corresponding view counts for each markdown file and
    language.
    """
    global ViewsData, views_by_mdtitle_langs, count_views_by_mdtitle, count_views_by_lang, views_by_lang

    # Iterate through each markdown file and language in `ViewsData`
    for mdtitle, langs in ViewsData.items():

        # Create a dictionary to store the view counts for a given markdown file
        views_by_mdtitle_langs[mdtitle] = {}
        count_views_by_mdtitle[mdtitle] = 0

        # Iterate through each language for a given markdown file
        for lang, v in langs.items():

            views_by_mdtitle_langs[mdtitle][lang] = v['views']

            # Add the view count
            count_views_by_mdtitle[mdtitle] += v['views']

            # If the language doesn't exist in `count_views_by_lang`, add it
            if not lang in count_views_by_lang: count_views_by_lang[lang] = 0

            # Increment the total view count for the given language
            count_views_by_lang[lang] += v['views']

            # If the language doesn't exist in `views_by_lang`, add it
            if not lang in views_by_lang:   views_by_lang[lang] = {}

            # Add the view count
            views_by_lang[lang][v['title']] = v['views']
#---
makeviews()
#---
if __name__ == '__main__':
    print(f'len of views_by_mdtitle_langs: {len(views_by_mdtitle_langs)}')
    print(f'len of count_views_by_mdtitle: {len(count_views_by_mdtitle)}')
    print(f'len of count_views_by_lang: {len(count_views_by_lang)}')
    print(f'len of views_by_lang: {len(views_by_lang)}')
#---