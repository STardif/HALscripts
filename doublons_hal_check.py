#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:24:41 2019

@author: st242386 (samuel.tardif@cea.fr)
@date: 2018-02-13
 
The purpose of the script is to identify possible doubles in the list of 
publications from HAL for a given laboratory.

It gets the list of publications from a http request to the haltools server and
compares every possible pair by (1) title fuzzy matching and then (2) by 
comparing the DOI (if any)

The parameters for getting the publications list are (see top paragraph):
    annee_publideb : year  (e.g. '2014')
    annee_publifin : year  (e.g. '2050')
    struct : code for the laboratory (e.g. '40368' for MEM/NRS)

No warranties are made on the accuracy or exhaustivity of the results !
"""


###############################################
# EDIT HERE
# Publications Search Parameters
params = {'annee_publideb' : 2014,
          'annee_publifin' : 2050,
          'struct' : 40368}

# Title correlation threshold (100 = full match, 0 = no match)
title_correlation_threshold = 85 
###############################################



# BELOW IS THE ACTUAL SCRIPT

# Imports
import urllib
from bs4 import BeautifulSoup
from numpy import arange
from fuzzywuzzy import fuzz

# quick formatting, make sure all is in string format
for p in params: params[p] = str(params[p])

# additional parameters
add_params = {'typdoc' : '(%27ART%27,%27OUV%27,%27COUV%27,%27DOUV%27,%27COMM%27,'+\
                              '%27PATENT%27,%27OTHER%27,%27UNDEFINED%27,%27THESE%27,'+\
                              '%27HDR%27)',
              'CB_auteur' : 'oui',
              'CB_titre' : 'oui',
              'CB_article' : 'oui',
              'CB_DOI' : 'oui',
              'langue' : 'all',
              'tri_exp' : 'titre',
              'ordre_aff' : 'TA',
              'CB_rubriqueDiv' : 'oui',
              'Fen' : 'Aff'}


#build the url for the request
link = "http://haltools.archives-ouvertes.fr/Public/afficheRequetePubli.php?"
link = '&'.join([link]+['{}={}'.format(p,params[p]) for p in params])
link = '&'.join([link]+['{}={}'.format(p,add_params[p]) for p in add_params])
print("using this url for the request :")
print(link)
print('\n')


# get the list from haltools and parse it 
html = urllib.request.urlopen(link).read()
ph = BeautifulSoup(html, features = "lxml") # parsed html
refs = ph.find_all('dl') # list of all references
print("Found {:} references".format(len(refs)))
print('\n')

print("Matching title threshold = {:}%".format(title_correlation_threshold))
print('\n')



def get_doi(ref):
    """
    Extract the DOI for a given reference
    since there is no DOI field, I parse the dx.doi.org url (if any!)
    NOTE: Might be a possible confusion if there are supplementary materials with
    their own DOI ?? 
    
    input : 
        ref : dl tag 
    """
    doi = None
    # if the DOI field is present
    if 'CB_DOI' in add_params.keys():
        for dd in ref.find_all('dd'):
            if len(dd.contents[0]) > 3:
                if dd.contents[0][:3] == 'DOI':
                    doi = dd.contents[1].contents[0].lower()
    else:
        # brute force : list all urls in the tag and find the first matching one
        for atag in ref.find_all('a'):
            if atag['href'].startswith('https://dx.doi.org/'):
                doi = atag['href'][len('https://dx.doi.org/'):].lower()
                break
    return doi



def print_double(ref1, ref2):
    """
    Do the display part for matching references
    
    input : 
        ref1 : dl tag 
        ref2 : dl tag 
    """
    print('ref {:>3} : '.format(iii), ref1.dd.string)
    print('ref {:>3} : '.format(jjj), ref2.dd.string)
    print('correlation: ', correl)
    print('DOI 1 : ', get_doi(ref1))
    print('url originale: ', (ref1.a)['href'])
    print('url hal:', (ref1.a)['href'].replace('hal.univ-grenoble-alpes.fr',
                                               'hal.archives-ouvertes.fr'))
    print('DOI 2: ', get_doi(ref2))
    print('url originale: ', (ref2.a)['href'])
    print('url hal:', (ref2.a)['href'].replace('hal.univ-grenoble-alpes.fr',
        'hal.archives-ouvertes.fr').replace('hal-cea','hal'))
    print('\n')
	
	
	
# counters for the statistics
doi_double = 0
missing_doi_double = 0
title_double = 0


# loop over all refs and check matching titles
for iii in arange(len(refs)-1):
    doi1 = get_doi(refs[iii])            
    for jjj in arange(iii+1, len(refs)):
        # compute the matching rate
        correl = fuzz.ratio(refs[iii].dd.string, refs[jjj].dd.string)
        if correl > title_correlation_threshold :
            doi2 = get_doi(refs[jjj])                
            
            # DOI match = obvious double
            if doi1 != None and doi2 != None and doi2 == doi1:
                print('-'*20)
                print('!!!! DOUBLE FOUND (DOI match) !!!!')
                print_double(refs[iii], refs[jjj])
                doi_double += 1
                
            # only title match = possible double
            # not matching doi
            elif doi1 != None and doi2 != None and doi2 != doi1:
                print('-'*20)
                print('! Possible match (but different doi) !')
                print_double(refs[iii], refs[jjj]) 
                title_double += 1               
                
            # only title match = possible double
            # missing doi
            elif doi1 == None or doi2 == None:
                print('-'*20)
                print('!!! Possible match (missing DOI to confirm) !!!')
                print_double(refs[iii], refs[jjj])
                missing_doi_double += 1
            
print('#'*20)
print('found {:} DOI doubles'.format(doi_double))
print('found {:} possible doubles (no DOI to confirm)'.format(missing_doi_double))
print('found {:} title doubles but with different DOI'.format(title_double))

        
            

            
