import spacy
import pyspark
import sys
import numpy
from pprint import pprint
import json

class SpacyLoader:

    _loaded = {}
    counter = 0

    @classmethod
    def load(cls, lang):
        if lang not in cls._loaded:
            cls._loaded[lang] = spacy.load(lang)
            cls.counter += 1
        return cls._loaded[lang]


def spacy_process(string):
    nlp = SpacyLoader.load('en')

    text = json.loads(string)['text']
    sents = [s.text for s in nlp(text).sents]
    return filter(lambda x: x != "", sents)
    # return


conf = pyspark.SparkConf().setAppName("EntityFetcher")
sc = pyspark.SparkContext(conf=conf)

if len(sys.argv) == 1:
    test_file_path = "/home/vromanov/wiki/EnWiki/AA/wiki_00"
else:
    test_file_path = sys.argv[1]

text = sc.textFile(test_file_path)

pprint(text.flatMap(lambda x: spacy_process(x)).saveAsTextFile("out.txt"))
