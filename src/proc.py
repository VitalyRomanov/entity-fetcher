import spacy
import json
import sys

if len(sys.argv) == 1:
    test_file_path = "/home/vromanov/wiki/EnWiki/AA/wiki_00"
else:
    test_file_path = sys.argv[1]

texts = map(lambda x: json.loads(x)['text'], open(test_file_path).readlines())

nlp = spacy.load("en")

for text in texts:
    for s in nlp(text).sents:
        print(s)

    break