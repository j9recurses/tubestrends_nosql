## python 2.7.5
## Primary Author: Xavier Malina
## Email: xmalina@berkeley.edu
## Contributing Author: Janine Heiser
##This code was created as part of a Final Project for 'Info 290T-03: Data
##Mining and Analytics in Intelligent Business Services', a class offered in
##Spring 2014 at the School of Information at the University of California,
##Berkeley

# This code was written to transform JSON files containing the trending terms
# scraped from each web platform under consideration and transform them for
# similarity comparisons as well as eventual regression analysis.

import json
import glob
import fileinput
from os import listdir
import os
from os.path import isfile, join
import csv
import time
import logging
import chardet
import ast
##from string import punctuation
##import guesslanguage
##from pprint import pprint
import csv

# Bad Punctuation defined here so that we an remove or add specific characters
# if we find them to be important (For instance, the hashtag could end up
# being something we want to keep).
badpunctuation = '!"$%?&\'()*+\",.:;<=>[\\]/^`{|}~'

#These are pieces of punctuation that will be allowed to remain in the trend,
#if we want any.
acceptedpunctuation='#_-@'

#Covers all punctuation, for testing purposes
allpunctuation='!"$%?&\'()*+,.:;<=>[\\]^`{|}~#_-/@'

#List the current directory, so you can see if you're in the right one.
print os.getcwd()


currentdir = os.getcwd()

'''This portion defines empty dictionaries, lists that the functions will fill. 
#TO DO: Structure in a way that avoids setting universal variables'''

#This dictionary will be in the format key='platform name', 
#value=list of dictionaries, each of the format key=date, value=list of all terms that
#occurred on that network that day
networkdict={}

#This dictionary will capture all terms that failed encoding under every
#possible encoding format, i.e. the terms that came in were essetially
#corrupted or used some kind of 'non-standard' encoding
excepteddict={}

#This dictionary will capture for each term, which platforms it appeared on, on which days
termdict={}


alltrends=[]
uniqueterms=[]

#a list of all dates
alldates=[]


#creating sites as a list makes it easy to test for each one individually, good for testing
sites=['google','yahoo','instagram','youtube'] 





'''This function creates a loop to run through all JSON files available.'''
def extract_jsons(howmany=0):
    i = 0

    for step in os.walk(currentdir):           
                 
            for folder in step:                    

                    if len(folder)==0  or folder[0:3]=='C:\\':
                        pass
                    
                    else:
                        folderpath = step[0]
                        
                        for file in folder:
                            
                            if file.endswith('.json'):
                                site= file.split('_')[0]                               
                                get_dict(site,folderpath+'\\'+file)


'''This function aims to begin filling the above dictionaries, 
once for each jsonfile being passed to it'''

def get_dict(site,jsonfile):

    if site not in sites:
        return


    sitedict={}
    datedict={}
    
    excepteddict[site]=[]    
    termlist=[]   

    originaljson = json.loads(open(jsonfile,'r').readline())    
    
    #Here's where we begin to deal with encoding.
    json_data = [dict((k.encode('ascii'), v) for (k, v) in original.items()) for original in originaljson ]

    for k in range(1,len(json_data)):

        title='title'
        #JSONS have the term stored under 'title', 
        # except for Instagram, which was accidentally stored as 'caption'
        # this piece of code is a hardcoded way to account for that. 
        #TO DO: Make this agnostic to the label for the key under which the trend is stored

        term=json_data[k].get(title,'caption')

        if term =='caption':
            title='caption'
            term = json_data[k][title]
                
        #Some terms mysteriously stored are empty or contain just a period
        #TO DO: Explore why this is happening
        if term == '' or term=='.':            
            date=json_data[k]['the_date'].encode('utf-8')

            # Add current date to 'alldates' list if it's not already there for these weird ones...
            if date not in alldates:                
                alldates.append(date)

        else:  

            # this try/except excepts if chardet is not able to encode the trend term correctly
            #in which case the term is added to the 'excepteddict' dictionary for analysis at a later time          
            try:
                term=json_data[k][title].encode('utf-8')                
                              
                term=term.lower().replace("'s",'').replace("-"," ").replace("_"," ").replace('\\n','').translate(None, badpunctuation)
                term=' '.join(term.split())

##                #catch trends without punctuation...
##                if any([c in badpunctuation for c in term]):
##                    nonpunc='abcdefghijklmnopqrstuvwxyz0123456789'
##                    if any ([c in nonpunc for c in term]):
##                        pass
##                    else:
##                        print term
##                        break                

                #the JSON code defaults to decoding in UTF-8, so this encodes for UTF-8
                date=json_data[k]['the_date'].encode('utf-8')

                 # Add current date to 'alldates' list if it's not already there
                if date not in alldates:                    
                    alldates.append(date)
                   
                #We resorted to the chardet library to handle encoding issues.
                charend = chardet.detect(term)['encoding']

                if charend==None:
                    pass

                else:                
                    # print term
                    term = term.encode(charend)
                    termlist.append(term)

                    
            except:                 
                
                term=json_data[k][title].encode('utf-8')
                date=json_data[k]['the_date'].encode('utf-8')
                
                if date not in alldates:
                    alldates.append(date)
                
                excepteddict[site].append(term)
                term = '_UNKNOWN'
                pass

    
    '''Having extracted and attempted to encode all terms in this JSON file,
    generate a unique list of those terms and pass them back to the allterms' list'''

    uniqueterms = (list(set(termlist))
    alltrends.extend(uniqueterms)


    ##this portion creates reflects the most imporant part of the code: the
    ##structure for the platform dictionary.   Determining the needed
    ##structure that would be able to answer our questions  was a large
    ##component of this project

    datedict={}
    datedict[date]=uniqueterms
    
    if site not in networkdict.keys():        
        networkdict[site]={}
    else:
        networkdict[site][date]=datedict[date]

    ##    print len(sitedict[site][myd[k]['the_date']])

'''This Function generates the dictionary in which the trend terms 
are the key, essentially transforming the platform dictionary'''

def get_term_dict(sites,terms,dates=''):


    #this catches in the case that a singular date is input instead of a list   
    if type(dates) is str :        
        dates=list(dates)

    terms=sorted(terms)   

    i=0

    #assumes the terms input is a list of all terms that we are interested in
    for term in terms:
        
        datedict={}
        for date in dates:

            sitedict={}
            for site in sites:                    
                            
                if date not in networkdict[site].keys():
                    
                    sitedict[site]=0

                
                elif term in networkdict[site][date]:
                    if term == 'dani alves':
                        print 'dani'
                        print site
                    
                    #this sets as a dummy variable for 'present on platform on that day' or not
                    sitedict[site] = 1
                else:
                    sitedict[site] = 0

            if sitedict['google']==1 and sitedict['youtube']==1:
                print term
            datedict[date]=sitedict
            
                
        termdict[term]=datedict



''' This function was built to support the regression analysis, as well 
as more superficial analysis by converting the above dictionaries into 
a format that is saved as a CSV, as our teammembers found that having it
 in this format would be more easily understandable based on their experience'''


def saveToCsv(dict, sites, dates, terms, limit=100000):

 
    for date in dates:

        with open(date+'.csv', 'wb') as csvfile:
        
            outputfile=csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)

            headers=['term']
            headers.extend(sites)
            outputfile.writerow(headers)
            
            for term in sorted(terms):
                row=[term.replace(',',' ')]
                if date not in dict[term].keys():
                    
                    [row.append(0) for site in sites]
                    
                else:
                    
                    [row.append(dict[term][date][site]) for site in sites]

                outputfile.writerow(row)

        csvfile.close()

print 'starting...'

extract_jsons()

print 'got jsons for sites %s, and create site dictionary' % sites

get_term_dict(sites,alltrends,alldates)

print 'generated term dictionaries for all terms'


'''Output as JSON files the dictionaries we just created, for ease of use and transfer'''

print 'saving termdict to text file in %s named %s' %(currentdir, 'termdict.txt')

termdicttext = open('trenddict.json','w')
json.dump(termdict,termdicttext)
termdicttext.close()

print 'saving networkdict to text file in %s named %s' %(currentdir, 'network_dict.txt')
networktext = open('networkdict.json','w')
json.dump(networkdict,networktext)
networktext.close()

print 'saving list of all uniqueterms to text file in %s named %s' %(currentdir, 'allterms.txt')

alltrends=sorted(list(set(alltrends)))
all_trend_terms = open('all_trend_terms_wspaces.txt','w')
all_trend_terms.write(str(alltrends))
all_trend_terms.close()

print 'all done'


'''This last section exists for the purpose of creating a csv 
in the format requested by one of our teammates to 
perform the Jaccard similarity analysis'''

cosinedict={}


for site in networkdict.keys():
    siteterms=[]
    for date in networkdict[site].keys():
        siteterms.extend(networkdict[site][date])
    siteterms=sorted(list(set(siteterms)))
    cosinedict[site]=siteterms

##print cosinedict.keys()

##print 'saving networkdict with dates flattened to text file in %s named %s' %(currentdir, 'networkdictflat.txt')
##flattext = open('networkdictflat.json','w')
##json.dump(cosinedict,flattext)
##
##networktext.close()

print 'All done! Congratulations you are officially a Data Miner!'

    
##saveToCsv(termdict, sites, alldates, alltrends)


