from __future__ import division
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from itertools import combinations
from collections import defaultdict
from math import sqrt
import string
from decimal import Decimal

class CosineSim(MRJob):

   INPUT_PROTOCOL = JSONValueProtocol

   def extract(self, _, record):    
      title = ''  
      sdoid  = record['sdoid']
      ##pull out instagram, which have a separate tag/caption
      if sdoid == "4":
         try:
            title = record['title'].encode("utf-8")
            if len(title) == 0:
               title = record['tags'].encode("utf-8")
         except Exception: 
            pass
         tlen = len(title)
         if tlen == 0:
            try:
               title = record['caption'].encode("utf-8")
            except Exception: 
               pass
      else: 
         try:
            title = record['title'].encode("utf-8")
         except Exception: 
            pass
      exclude = set(string.punctuation)
      title = ''.join(ch for ch in title if ch not in exclude)
      title = title.strip('#')
      title = title.strip('@')
      yield [ record['sdoid'], title]


   def combine(self, sdoid, titles):
      yield [sdoid, list(titles)]
   
   
   def word_freq(self, sdoid, title_list):
      totalterms = len(title_list)
      freq = defaultdict(Decimal)
      for term in title_list:
         freq[term] += 1 / Decimal(totalterms)
      yield["all", [sdoid, freq]]

   def compare_vectors (self, _, freq):
      #print "in here!!!!!"
      #make a dict to store the output
      final_output = {}
      #get a list of sdoids to use for combos
      mydoclist = []
      #make a big dictionary to store all the text
      mydictall = {}
      for k in freq:
         mydictall[k[0]] = k[1]
         mydoclist.append(k[0])
         #make the combos to
      combos = list(combinations(mydoclist, 2))
      #print "*******All combos to iterate through*************"
      #print combos
         ##iterate through all the possible combinations of documents
      for c in combos:
         #print "***Combinations: "  + str(c) + '*********'
            #get a big list of words

         #print "*******ALL WORDS*******"
         all_words = list(set(mydictall[c[0]]).union(set(mydictall[c[1]])))
         #all_words = list(mydictall[c[0]].union(mydictall[c[1]]))
     
         frequency_vector1 = [mydictall[c[0]].get(word, 0) for word in all_words]
            #print frequency_vector1
         frequency_vector2 = [mydictall[c[1]].get(word, 0) for word in all_words]
            #print frequency_vector2

         #first get the dot product- this is the numerator
         dot_product_v1v2 = sum(a * b for a, b in zip(frequency_vector1, frequency_vector2))
         #print "here"
         #print dot_product_v1v2
         #print "**"
         dot_product_v1 =  sum(a * b for a, b in zip(frequency_vector1, frequency_vector1))
         #print dot_product_v1
         dot_product_v2 =  sum(a * b for a, b in zip(frequency_vector2, frequency_vector2))
         #print dot_product_v2

         #then get the magnitude for each vector
         v1magnitude =  sqrt(dot_product_v1)
         #print v1magnitude
         v2magnitude =  sqrt(dot_product_v2)
         #print v2magnitude
         #print "****more***"
         #print (v1magnitude * v2magnitude)
         #print "********"
         cosine_sim = (dot_product_v1v2) / (v1magnitude * v2magnitude)
         #print "***right here***"
         newc = ":".join(c) 
         mycosine = str(cosine_sim)
         yield[newc, mycosine]
            
   ## Measure similarity --> some methods
   '''
   def dot_product(v1, v2):
      """Get the dot product of the two vectors.
      if A = [a1, a2, a3] && B = [b1, b2, b3]; then
         dot_product(A, B) == (a1 * b1) + (a2 * b2) + (a3 * b3) The above will return true; Also input vectors must be the same length. """
      return sum(a * b for a, b in zip(v1, v2))

   
   def magnitude(vector):  
      """Returns the numerical length / magnitude of the vector."""
      return sqrt(dot_product(vector, vector))

   
   def similarity(v1, v2):
      """Ratio of the dot product & the product of the magnitudes of vectors."""
      return dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))
   '''

   def steps(self):
      return [self.mr(mapper=self.extract, reducer=self.combine), 
            self.mr(mapper=self.word_freq, reducer=self.compare_vectors)]



if __name__ == '__main__':
   CosineSim.run()