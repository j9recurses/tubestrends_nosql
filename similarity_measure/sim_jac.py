from __future__ import division
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from itertools import combinations
from collections import defaultdict
from math import sqrt
import string

class SimJac(MRJob):

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
      yield [sdoid, list(set(titles))]
   
   
   def distribute(self, sdoid, title_list):
      #print sdoid, title_list
      yield 'all', [sdoid, title_list]

   def compare(self, _, title_list):
      for (sdoid_a, titles_a), (sdoid_b , titles_b) in combinations(title_list, r=2):
         sim = SimJac.jaccard(titles_a, titles_b)
         combo =  sdoid_a + ":" + sdoid_b 
         yield [ combo, sim]
   
   
    ## Measure jac similarity

   @staticmethod
   def jaccard(titles_a, titles_b):
      return float(len(set(titles_a) & set(titles_b))) / len(set(titles_a) | set(titles_b))

   def steps(self):
      return [self.mr(mapper=self.extract, reducer=self.combine), 
            self.mr(mapper=self.distribute, reducer=self.compare)]



if __name__ == '__main__':
   SimJac.run()