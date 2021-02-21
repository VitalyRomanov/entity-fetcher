# cluster words based on the adjective with which they co-occur

# do this using LDA, parse every sentence in such a way that verbs ans adjectives and nouns are grouped together
from nltk_wrapper import NltkWrapper
from nltk import sent_tokenize
import json
import argparse
import sys
from pprint import pprint

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

nlp = NltkWrapper(LANG_CODE)

with open("chunk_verbs_1g.txt", "w") as sink:

    for line in sys.stdin:
        if line:

            try:
                line = " ".join(json.loads(line)['text'].split("\n"))
            except:
                pass

            for s in nlp.sentencize(line):

                # s = line.strip()

                # for s in sent_tokenize(line, LANG):
                #     s = lowercase_first(s)

                chunk_parsed = nlp.noun_chunks(s)
                verbs = [t[0] for t in chunk_parsed.leaves() if t[1] == "VERB"]
                chunks = ([t[0] for t in c.leaves()] for c in chunk_parsed.subtrees() if "NP" in c.label())
                # print(verbs)
                # print(chunk_parsed)
                # pprint()
                for c in chunks:
                    # print(c + verbs)
                    sink.write("%s\n" %" ".join(c + verbs))
