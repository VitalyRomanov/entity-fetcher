# from LentaReader import LentaReader
import sys

# import spacy

sys.path.insert(0, "/Volumes/External/dev/")

from LanguageTools import Tokenizer
from LanguageTools.PyMyStemTagger import PyMyStemTagger
from PatternDetector import PatternDetector
from HyponymExtractor import HyponymDetector
from LanguageTools import WikiLoaderv2

# from LanguageTools.syntaxnet_wrapper.tokenizer_ru import create_tokenizer_ru

LANG = 'english'
LANG_CODE = 'en'


def prep_for_SN(sent):
    s = sent.strip()
    if s[-1] in {".", "."}:
        s = sent[:-1] + " ."

    return tok(sent, split=False)

def print_result(result):
    for sent in result:
        for word in sent:
            print(word.word_form, word.link_name, sent[word.parent].word_form, word.pos_tag)
        print("")


# lentaPath = sys.argv[1]


# lr = LentaReader(lentaPath)
tok = Tokenizer.Tokenizer()
# tag = Tagger.Tagger()
stok = Tokenizer.PunctTokenizer()
# pd = PatternDetector('ru')
hyp = HyponymDetector(LANG_CODE)
# tagger = PyMyStemTagger()

from nltk import pos_tag, word_tokenize, sent_tokenize
from pprint import pprint
from nltk.tag.mapping import map_tag
from nltk import RegexpParser
from nltk import chunk
from nltk.tag import CRFTagger
from nltk.chunk import conlltags2tree

from collections import Counter

def dump_concepts(concepts):
    with open("concepts_cryptonews.txt", "w") as concept_file:
        for ((sup, sub), count) in concepts.most_common(len(concepts)):
            concept_file.write("{}\t{}\t{}\n".format(sup, sub, count))


import sys
import pickle
_, articles = zip(*pickle.load(open(sys.argv[1], "rb")))
articles = list(articles)


debug_file = open("debug_cryptonews.txt", "a")

concepts = Counter()
count = 0

for doc in articles:

    for line in doc.split("\n"):

        if line:
            for s in sent_tokenize(line, LANG):
                ts = pos_tag(word_tokenize(s, LANG, preserve_line=True), lang='eng')
                candidates = hyp(ts)
                for c in candidates:
                    debug_file.write("{}; {};\t{}\n".format(c[0], c[1], s))
                    print(c)
                    if "\n" in s:
                        print(s)
                concepts |= Counter(candidates)


    
    # doc = wiki.next_doc()
    # break
    count += 1
    if count % 100 == 0:
        dump_concepts(concepts)        

dump_concepts(concepts)

