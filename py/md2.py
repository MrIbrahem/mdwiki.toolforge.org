#!/usr/bin/python

"""

تجربة ملف mdd.py

python pwb.py md2 -page:Hyoscine_butylbromide
python3 pwb.py md2 -page:Hyoscine_butylbromide

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import urllib
import codecs
#---
import pywikibot
import re
import sys
#---
sys_argv = sys.argv or []
pywikibot.output(sys_argv)
#---
import mdwiki_api
from TDpynew import mdd
#---
def treat_page( title, textn ):
    #---
    newtext = mdd.work( title , returntext = True , text_O = textn )
    #---
    if 'test' in sys_argv: 
        pywikibot.showDiff( textn , newtext )
        return ''
    #---
    mdwiki_api.page_putWithAsk( textn , newtext , 'mdwiki changes.' , title , False )
    #---
    test_text = '''
{{Drugbox
| Verifiedfields = changed
| verifiedrevid = 448004176
| image = Abacavir and lamivudine.svg
| width = 200

<!--Combo data-->
| type = combo
| component1 = Abacavir
| class1 = Nucleotide analogue [[reverse transcriptase inhibitor]]
| component2 = Lamivudine
| class2 = Nucleotide analogue [[reverse transcriptase inhibitor]]

<!--Names-->
| pronounce = 
| tradename = Kivexa, Epzicom, others
| synonyms = 
| IUPAC_name =

<!--Clinical data-->
| pregnancy_AU = <!-- A / B1 / B2 / B3 / C / D / X -->
| pregnancy_US = C
| routes_of_administration = by mouth
| onset = 
| duration_of_action = 
| defined_daily_dose = is not established<ref name=who/>
 
| MedlinePlus = a696011
| pregnancy_category =  
| legal_AU = S4
| legal_CA = <!-- Schedule IV{{citation needed|date=July 2019}} -->
| legal_UK = POM
| legal_US = Rx-only
| legal_status =

<!--Chemical data-->
|drug_name=|alt=|caption=|licence_EU=|licence_US=}}
'''
#---
def main():
    #---
    ttab = []
    #---
    # python3 pwb.py md2 -page:Abacavir/lamivudine
    # python3 pwb.py md2 -page:Hyoscine_butylbromide
    #---
    for arg in sys_argv:
        arg, sep, value = arg.partition(':')
        #---
        if arg == "-page" : 
            ttab.append(value)
        #---
        # python3 pwb.py md2 allpages
        # python pwb.py md2 allpages
        if arg == "allpages" : 
            ttab = mdwiki_api.Get_All_pages( '!' , namespace = '0', apfilterredir = 'nonredirects' )
    #---
    numb = 0
    #---
    for title in ttab:
        numb += 1
        pywikibot.output( '<<lightyellow>> tit:%d / %d\t title: %s.' % ( numb , len(ttab) , title )  )
        text = mdwiki_api.GetPageText(title)
        treat_page( title , text )
    #---
    # python pwb.py md2 test
    if 'test' in sys_argv:
        treat_page( 'nana' , test_text )
        
#---
if __name__ == '__main__':
    main()
#---