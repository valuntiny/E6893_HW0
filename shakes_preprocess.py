#!/usr/bin/env python

import pyspark
import sys
import nltk

nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
stop_words=set(stopwords.words('english'))
import string
list_punct=list(string.punctuation)

if len(sys.argv) != 2:
  raise Exception("Exactly 1 arguments are required: <inputUri>")

inputUri=sys.argv[1]

def word_tokenize1(x):
    lowerW = x.lower()
    return nltk.word_tokenize(x)

sc = pyspark.SparkContext()
lines = sc.textFile(sys.argv[1])
words = lines.flatMap(word_tokenize1)\
.filter(lambda word : word[0] not in stop_words and word[0] != '')\
.filter(lambda punct : punct not in list_punct)

wordCounts = words.map(lambda word: (word, 1))\
.reduceByKey(lambda count1, count2: count1 + count2)\
.map(lambda kv: (kv[1], kv[0]))\
.sortByKey(ascending=False)\
.take(5)

for (count, word) in wordCounts:
        print "%i: %s" % (count, word)