#!/usr/bin/python
#pm = __import__('cosine_reduce')

import os
from os import listdir
from os.path import isfile, join
import subprocess
from decimal import Decimal
import collections


def minmax_normalize(value,minz,maxz):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    minz = float(minz)
    value = float(value)
    maxz = float(maxz)
    mynorms = (value - minz)/(maxz-minz)
    return round(mynorms,6)


def mymin(contribs):
    min_contribs = sorted(contribs, key=float)   
    return min_contribs[0]

def mymax(contribs):
    max_contribs = sorted(contribs, key=float, reverse=True)       
    return max_contribs[0]


def make_dicts(reducedout, dictype, mypath):
##first, get everything into a dict by day terms
	mytotaldict = dictype
	rfiles =  mypath + "/" + reducedout
	reducedonlyfiles = [ f for f in listdir(rfiles) if isfile(join(rfiles,f))]	
	#print reducedonlyfiles
	for file in reducedonlyfiles: 
		day = file.split(".txt")
		day  = day[0]
		day = day.split("_")
		day = day[0]
		with open(rfiles+ file) as f:
			anotherdict= {}
			for line in f:
				stuff = line.split("\t")
				combo =  stuff[0].strip('"')
				cosineval = stuff[1].strip("\n").strip('"')
				anotherdict[combo] = cosineval
			mytotaldict[day] = anotherdict
	return(mytotaldict)

def make_closer_dic(mytotaldict_type, alldays):
	finaldict = collections.OrderedDict()
	od = collections.OrderedDict(sorted(mytotaldict_type.items()))
	for k,v in od.iteritems():
		alldays.append(k)
		network_combo = v.keys()
		for zk in network_combo:
			if zk not in finaldict:
				finaldict[zk] = [v[zk]]
			else:
				coslist = finaldict[zk]
				coslist.append(v[zk])
				finaldict[zk] = coslist
	return finaldict

def make_files_norms(final_file_out, alldays, finaldict):
	#write a file
	fcos= open(final_file_out+"_normalized.csv",'w')
	print fcos
	#header row
	alldays =  "network_combination,"+ ",".join(alldays)
	fcos.write(alldays +'\n')
	for k,v in finaldict.iteritems():
		lastlist = []
		lastlist.append(str(k))
		#normalize the results so that we can compare the social networks to one another. 
		minval = mymin(v)
		maxval = mymax(v)
		for vv in v:
			if float(maxval) > 0.0:
				normalv = minmax_normalize(vv,minval,maxval)
				lastlist.append(normalv)
			else:
				lastlist.append(vv)
		finalstuff = map(str, lastlist)
		finalstuff = ",".join(finalstuff)
		fcos.write(finalstuff+ '\n')
	fcos.close()


def make_files_reg(final_file_out, alldays, finaldict):
	#write a file
	fcos= open(final_file_out + ".csv",'w')
	#header row
	alldays =  "network_combination,"+ ",".join(alldays)
	fcos.write(alldays +'\n')
	for k,v in finaldict.iteritems():
		lastlist = []
		lastlist.append(str(k))
		for vv in v:
			lastlist.append(vv)
		finalstuff = map(str, lastlist)
		finalstuff = ",".join(finalstuff)
		fcos.write(finalstuff+ '\n')
	fcos.close()


def run_commands(onlyfiles):
	for file in onlyfiles:
		if file.endswith(".json"):
			new_name = file.split("_")
			new_name = new_name[0]
			cmdcos_term = 'python cosine_reduce.py ' + file + " > " + reducedoutcos_term + new_name + "_cos_term.txt"
			coolcos_term = os.system(cmdcos_term)
			cmdjac_term = 'python sim_jac.py ' + file + " > " + reducedoutjac_term + new_name + "_jac_term.txt"
			cooljac_term = os.system(cmdjac_term)
			cmdcos_word = 'python cosine_nospace.py ' + file + " > " + reducedoutcos_word + new_name + "_cos_word.txt"
			coolcos_word = os.system(cmdcos_word)
			cmdjac_word = 'python sim_jac_nospace.py ' + file + " > " + reducedoutjac_word + new_name + "_jac_word.txt"
			cooljac_word = os.system(cmdjac_word)

#get path of the current dir
mypath = os.path.dirname(os.path.realpath(__file__))

#set the directory for the mapreduce final out
reducedoutcos_term = 'filesreduced_cos_term/'
reducedoutjac_term = 'filesreduced_jac_term/'
reducedoutcos_word = 'filesreduced_cos_word/'
reducedoutjac_word = 'filesreduced_jac_word/'

#get a list of the files to reduce
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f))]
print onlyfiles

#iterate through all the files and run the mr job commands, put the output to the outdirs. 


#create dicts for each type of output
dict_cos_term = {}
dict_sim_term = {}
dict_cos_word = {}
dict_sim_word = {}

#create a list of all the days in each file type; don't know the order and we need 
#to save the order of dates so we can create the csv header

run_commands(onlyfiles)

#create a dict of the type dirs and the type dicts
all_types_dict =  {reducedoutcos_term: dict_cos_term, reducedoutjac_term:dict_sim_term, reducedoutcos_word: dict_cos_word, reducedoutjac_word:dict_sim_word }
#dir to write final results to
finalout_dir = mypath + "/final_results/"
print finalout_dir
for k,v in all_types_dict.iteritems():
	dictstuff = make_dicts(k, v, mypath)
	alldays = []
	dictstuff_closer = make_closer_dic(dictstuff, alldays)
	f_partname = k.split("_")
	f_partname = finalout_dir + f_partname[1] + "_"+ f_partname[2].strip("/")+ "_results"
	make_files_norms(f_partname, alldays,dictstuff_closer)
	make_files_reg(f_partname, alldays,dictstuff_closer)




