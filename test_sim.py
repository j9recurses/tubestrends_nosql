from collections import defaultdict
import re
from math import sqrt
import json

def remove_punctuation(text):
     return re.sub('[,.?";:\-!@#$%^&*()]', '', text)
 
def remove_common_words(text_vector):
    """Removes 50 most common words in the uk english.
 
        source: http://www.bckelk.ukfsn.org/words/uk1000n.html
 
        """
    common_words = set(['the', 'and', 'to', 'of', 'a', 'I', 'in', 'was',
        'he', 'that', 'it', 'his', 'her', 'you', 'as', 'had', 'with',
        'for', 'she', 'not', 'at', 'but', 'be', 'my', 'on', 'have', 'him',
        'is', 'said', 'me', 'which', 'by', 'so', 'this', 'all', 'from',
        'they', 'no', 'were', 'if', 'would', 'or', 'when', 'what', 'there',
        'been', 'one', 'could', 'very', 'an', 'who'])
    return [word for word in text_vector if word not in common_words]


def dot_product(v1, v2):
    """Get the dot product of the two vectors.

    if A = [a1, a2, a3] && B = [b1, b2, b3]; then
    dot_product(A, B) == (a1 * b1) + (a2 * b2) + (a3 * b3)
    true

    Input vectors must be the same length.

    """
    print  sum(a * b for a, b in zip(v1, v2))
    return sum(a * b for a, b in zip(v1, v2))


def magnitude(vector):
    """Returns the numerical length / magnitude of the vector."""
    return sqrt(dot_product(vector, vector))


def similarity(v1, v2):
    """Ratio of the dot product & the product of the magnitudes of vectors."""
    return dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))


def word_frequencies(word_vector):
    """What percent of the time does each word in the vector appear?
     Returns a dictionary mapping each word to its frequency.
    """
    num_words = len(word_vector)
    frequencies = defaultdict(float)
    for word in word_vector:
        frequencies[word] += 1.0 / num_words

    return dict(frequencies)


def compare_vectors(word_vector1, word_vector2):
    """Numerical similarity between lists of words. Higher is better.

    Uses cosine similarity.
    Result range: 0 (bad) - 1 (uses all the same words in the same proportions)

    """
    frequency_dict1 = word_frequencies(word_vector1)
   
    frequency_dict2 = word_frequencies(word_vector2)
    #print  frequency_dict2
    all_words = list(set(word_vector1).union(set(word_vector2)))
    print  len(all_words)

    frequency_vector1 = [frequency_dict1.get(word, 0) for word in all_words]
    #print frequency_vector1 
    frequency_vector2 = [frequency_dict2.get(word, 0) for word in all_words]
    #print frequency_vector1 
    return similarity(frequency_vector1, frequency_vector2)

def compare_texts(text1, text2):
    """How similar are the two input paragraphs?"""
    return compare_vectors(text1,text2)


#data1 = ['Jennifer Esposito', 'Jennifer Esposito', 'Spiderman 2', "stuff"]
#data2 = ['Jennifer Esposito', 'Jennifer Esposito', 'Spiderman 2']

ins = open( "final_out/20140428_combined.json", "r" )
array_insta = []
array_youtube = []
array_google = []
array_twitter = []
array_yahoo = []
ids =  []

for line in ins:
    d = json.loads(line)
    myi =  d['sdoid']
    if myi not in ids:
        ids.append(myi)
    if myi == "5":
        word = d['title']
        words = word.split(" ")
        for w in words:
            array_youtube.append( remove_punctuation(w.lower()))
    if myi == "2":
        word = d['title']
        words = word.split(" ")
        for w in words:
            array_google.append( remove_punctuation(w.lower()))
    if myi == "1":
        word = d['title']
        words = word.split(" ")
        for w in words:
            array_twitter.append( remove_punctuation(w.lower()))
    if myi == "4":
        word  = d['title']
        if len(word) == 0:
            word = d['caption']
        words = word.split(" ")
        for w in words:
            array_insta.append( remove_punctuation(w.lower()))
    if myi == "3":
        word = d['title']
        words = word.split(" ")
        for w in words:
            array_yahoo.append( remove_punctuation(w.lower()))
ins.close()


cool = compare_texts(remove_common_words(array_google),remove_common_words(array_twitter))
cool2 = compare_texts((array_google),remove_common_words(array_yahoo))
cool3 = compare_texts((array_insta),remove_common_words(array_youtube))
cool3 = compare_texts((array_google),remove_common_words(array_youtube))
print '********Final out***********'
print "google v twitter"
print cool

print '********Final out***********'
print "google v yahoo"
print cool2

print '********Final out***********'
print "insta"
print cool3

