#! /usr/bin/env python

from __future__ import division
from mrjob.job import MRJob
from itertools import combinations
import numpy as np
import sys
from collections import defaultdict


class Similarity(MRJob):



    def extract_incident(self, _, line):
        record = line.split(',')

        words = defaultdict(int)


        for i in record[1:]:
            words[i] += 1


        uniqueWords = words.keys()
        # sys.stderr.write("MAPPER OUTPUT: ({0},{1})\n".format(record[0],uniqueWords))

        yield record[0], uniqueWords




    def combine_incident(self, network, words):
        allwords = list(words)

        # sys.stderr.write("REDUCER INPUT: ({0},{1})\n".format(network,list(allwords)))

        yield network, list(allwords)


    def nextmapper(self, network, words):

        yield "this", [network, list(words)]


    def nextreducer(self, _, allnetworks):

        # yield "all", list(allnetworks)

        record = defaultdict(list)

        keys = []

        for i in allnetworks:
            if type(i) == 'list':

                record[i[0][0]] = i[0][1:][0]

                # keys.append(i[0][0])
            else:
                # keys.append(i[0])
                record[i[0]] = i[1][0]


        yield "all words", record.values()

        for k_a, k_b in combinations(record.keys(), r=2):

            num = len(list(set(record[k_a]) & set(record[k_b])))
            denom = len(list(set(record[k_a]) | set(record[k_b])))

            sim = float(num)/denom

            yield [k_a, k_b], sim










    def steps(self):
        """
        MapReduce Steps:

        extract_incident    :   <_, line>  =>  <incident, feature>
        combine_incident    :   <incident, [feature]> => <incident, allfeatures>
        map_incident        :   <incident, [incedentfeatures] => <"all", [[incident, features]]
        reduce_incident     :   <_, allincidents> => <[incident_pairs], similarity>
        """

        return [
            self.mr(mapper=self.extract_incident, reducer=self.combine_incident),
            self.mr(mapper=self.nextmapper, reducer=self.nextreducer)
        ]








if __name__ == '__main__':
    Similarity.run()
