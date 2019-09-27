#!/usr/bin/env python

import pyspark
import sys

if len(sys.argv) != 2:
  raise Exception("Exactly 1 arguments are required: <inputUri>")

inputUri=sys.argv[1]

sc = pyspark.SparkContext()
lines = sc.textFile(sys.argv[1])
words = lines.flatMap(lambda line: line.split())
wordCounts = words.map(lambda word: (word, 1))\
.reduceByKey(lambda count1, count2: count1 + count2)\
.map(lambda kv: (kv[1], kv[0]))\
.sortByKey(ascending=False)\
.take(5)

for (count, word) in wordCounts:
        print "%i: %s" % (count, word)