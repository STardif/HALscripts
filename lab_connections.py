#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:24:41 2019

@author: st242386 (samuel.tardif@cea.fr)
@date: 2018-02-13
 
The purpose of the script is to plot the connections (= common references) 
between two or more labs by comparing their respective scientific communications lists
"""

## example 1
#labs = {'MEM' : 460264,
#        'LETI' : 40214,
#        'LITEN' : 40221}
        
## example 2
#labs = {'NRS' : 40368,
#        'LSim' : 40364,
#        'MDN' : 40365,
#        'LEMMA' : 40362,
#        'SGX' : 460267,
#        'RM' : 40372}

# example 3
labs = {'NRS' : 40368,
        'LSim' : 40364,
        'LEMMA' : 40362,}

annee_publideb = 2014
annee_publifin = 2019


# Imports
import urllib
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt


def get_ref(struct):

    # Publications Search Parameters
    params = {'annee_publideb' : annee_publideb,
              'annee_publifin' : annee_publifin,
              'struct' : struct}
    
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
    return refs




def get_ref_list(labs):
    refs = {}
    for lab in labs : refs[lab] = get_ref(labs[lab])
    return refs



def get_overlap(lab1,lab2,refs):
    return len(set.intersection(set(refs[lab1]),set(refs[lab2])))


def plot_figure(labs,refs,
                radius_scale_factor = 0.03,
                txt_offset_scale_factor = 0.1,
                vertex_width_scale_factor = 1):
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111)
    #fig.patch.set_visible(False)
    ax.set_xlim((-1.5,1.5))
    ax.set_ylim((-1.5,1.5))
    ax.axis('off')
    ax.set_aspect('equal')
    
    nlabs = len(labs)            
    lab_circle={}
    ilab = 0
    for lab in labs:
        lab_circle[lab] = [np.cos(ilab*2*np.pi/nlabs),
                           np.sin(ilab*2*np.pi/nlabs),
                           np.sqrt(len(refs[lab]))*radius_scale_factor]
        ilab+=1
        
        
    done = []
    for lab1 in labs:
        done += [lab1]
        x1,y1,r1 = lab_circle[lab1][0],lab_circle[lab1][1],lab_circle[lab1][2]
        ax.add_artist(plt.Circle((x1, y1), r1, zorder=1,
                                 facecolor = 'w',
                                 edgecolor = 'k'))
        ax.text(x1,y1,lab1+'\n{:}'.format(len(refs[lab1])), 
                horizontalalignment='center',
                verticalalignment='center')
    
        for lab2 in labs:
            if lab1 != lab2 and lab2 not in done:
                x2,y2 = lab_circle[lab2][0],lab_circle[lab2][1]
                ol = get_overlap(lab1,lab2,refs)
                if ol > 0:
                    ax.plot([x1,x2],[y1,y2],lw=ol*vertex_width_scale_factor,
                            zorder=0,color='grey')
                    ax.text((x2+x1)/2-txt_offset_scale_factor*(y2-y1)/2,
                            (y2+y1)/2+txt_offset_scale_factor*(x2-x1)/2,
                            str(ol), 
                            horizontalalignment='center',
                            verticalalignment='center')                
                    #ax.text((x2+x1)/2-0.1*(y2-y1)/2,
                    #        (y2+y1)/2+0.1*(x2-x1)/2,
                    #        str(ol))
    
    ax.set_title('Total and common publications '+\
                 'between {:} and {:}'.format(annee_publideb,annee_publifin))          
    plt.show()


refs = get_ref_list(labs)
plot_figure(labs,refs,
                radius_scale_factor = 0.03,
                txt_offset_scale_factor = 0.0,
                vertex_width_scale_factor = 1)
