import sys
import argparse
from nltk import pos_tag, word_tokenize, sent_tokenize
from collections import Counter
from HyponymExtractor import HyponymDetector
import hashlib
import json


parser = argparse.ArgumentParser(description='Train word vectors')
parser.add_argument('language', type=str, default='en', help='Language: English or Russian')
args = parser.parse_args()

if args.language == 'en':
    LANG = 'english'
    LANG_CODE = 'en'
elif args.language == 'ru':
    LANG = 'russian'
    LANG_CODE = 'ru'
else:
    raise ValueError("This language is not supported:", args.language)


hyp = HyponymDetector(LANG_CODE)


dump_files = {
    'P1':open("concepts_p1.txt", "w"),
    'P2':open("concepts_p2.txt", "w"),
    'P3':open("concepts_p3.txt", "w"),
    'P4':open("concepts_p4.txt", "w"),
    'P5':open("concepts_p5.txt", "w"),
    'P6':open("concepts_p6.txt", "w"),
    'P7':open("concepts_p7.txt", "w")
}

sentense_bank = open("sentense_bank.txt", "w")
recorded_sentences = set()

concepts = Counter()
count = 0

print("******************")
print("Ready to extract")
print("******************")

def sentence_id(sentence):
    return hashlib.md5(sentence.encode('utf-8')).hexdigest()


def lowercase_first(sentence):
    if len(sentence)>1 and sentence[1].lower() == sentence[1]:
        return sentence[0].lower() + sentence[1:]
    else:
        return sentence

candidate_count = 0

for line in sys.stdin:
    if line:

        try:
            line = " ".join(json.loads(line)['text'].split("\n"))
        except:
            pass

        for s in sent_tokenize(line, LANG):
            s = lowercase_first(s)
            candidates = hyp(s)

            if candidates:
                sentence_record = {
                    "sent_id": sentence_id(s),
                    "text": s
                }
                sentense_bank.write("%s\n" % json.dumps(sentence_record))
                recorded_sentences.add(sentence_id)
                for c in candidates:

                    c['sent_id'] = sentence_record['sent_id']
                    dump_files[c['type']].write("%s\n" % json.dumps(c))

                    candidate_count += 1 
                    if candidate_count % 10000 == 0:
                        print("Found %d candidates" % candidate_count)
