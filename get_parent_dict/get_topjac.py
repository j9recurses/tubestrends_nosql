#!/usr/bin/python
#this script gets the 20 or so terms with the biggest parent dicts
import json
from decimal import Decimal

def mymin(contribs):
    min_contribs = sorted(contribs, key=Decimal)   
    return min_contribs[0]

def mymax(contribs):
    max_contribs = sorted(contribs, key=Decimal, reverse=True)       
    return max_contribs[0]

def mymean(contribs):
    mean_contribs = sum(contribs) * 1.0 / len(contribs)
    return  mean_contribs

def mymedian(contribs):
    sortz = sorted(contribs)
    lengthz = len(contribs)
    if not lengthz % 2:
        return (sortz[lengthz / 2] + sortz[lengthz / 2 - 1]) / 2.0
    return sortz[lengthz / 2]

def mystddev(contribs):
    meancontrib = mymean(contribs)
    variance = map(lambda x: (x - meancontrib)**2, contribs)
    avgvar = mymean(variance)
    import math
    standard_deviation = math.sqrt(mymean(variance))
    return standard_deviation

ins = open('jacardsimilarityterms.txt')
mydict = {}
lines = ins.readlines()
for l in lines:
	d = json.loads(l.replace("\'", '"'));
	mydict = dict(d)


newdict1 =  {}
newlist = []
mykeys = []
for key in mydict:
	 cool = mydict[key].keys()
	 newlist.append(len(cool))



mmin = round(mymin(newlist),3)
mmax = round(mymax(newlist),3)
mmedian = round(mymedian(newlist),3)
mmean = round(mymean(newlist),3)
mmstdv = round(mystddev(newlist),3)
print "Descriptive Statistics- All terms:"
print "Min: " + str(mmin)
print "Max: " + str(mmax)
print "Mean:" + str(mmean)
print "Median:" + str(mmedian)
print "Std_Dev:" + str(mmstdv)
print "Total Terms:"  + str(len(mykeys))


mykeys2 = []
lastlist = []
interesting_words = {}
for key in mydict:
	for key2 in mydict[key]:
		cool2 = mydict[key][key2]
		cool2 = float(cool2)
		if cool2 > 0.7:
			cool3 = mydict[key].keys()
			lastlist.append(len(cool3))
			mykeys2.append(mydict[key])
			word = key
			interesting_words[word] = len(cool3)

mmin = round(mymin(lastlist),3)
mmax = round(mymax(lastlist),3)
mmedian = round(mymedian(lastlist),3)
mmean = round(mymean(lastlist),3)
mmstdv = round(mystddev(lastlist),3)
print "Descriptive Statistics- Jaquard over 0.7:"
print "Min: " + str(mmin)
print "Max: " + str(mmax)
print "Mean:" + str(mmean)
print "Median:" + str(mmedian)
print "Std_Dev:" + str(mmstdv)
print "Total Terms:"  + str(len(mykeys2))
print "Interesting Words"
#print interesting_words
mysort = sorted(interesting_words.items(), key=lambda(k,v):(v,k))

for s in mysort:
	print "Term: " + s[0] + ":count: " + str(s[1]) + "\n"

