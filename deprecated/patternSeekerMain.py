from LentaReader import LentaReader
import sys

# import spacy

sys.path.insert(0, "/Volumes/External/dev/")

from LanguageTools import Tokenizer
from LanguageTools.PyMyStemTagger import PyMyStemTagger
from PatternDetector import PatternDetector
from HyponymExtractor import HyponymDetector
from LanguageTools import WikiLoaderv2

# from LanguageTools.syntaxnet_wrapper.tokenizer_ru import create_tokenizer_ru



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


lentaPath = sys.argv[1]


lr = LentaReader(lentaPath)
tok = Tokenizer.Tokenizer()
# tag = Tagger.Tagger()
stok = Tokenizer.PunctTokenizer()
pd = PatternDetector('ru')
hyp = HyponymDetector('ru')
tagger = PyMyStemTagger()

from nltk import pos_tag, word_tokenize, sent_tokenize
from pprint import pprint
from nltk.tag.mapping import map_tag
from nltk import RegexpParser
from nltk import chunk
from nltk.tag import CRFTagger
from nltk.chunk import conlltags2tree

from collections import Counter

def dump_concepts(concepts):
    with open("concepts.txt", "w") as concept_file:
        for ((sup, sub), count) in concepts.most_common(len(concepts)):
            concept_file.write("{}\t{}\t{}\n".format(sup, sub, count))

wiki = WikiLoaderv2.WikiDataLoader("/Volumes/Seagate/language data/ru_wikipedia/articles/")
doc = wiki.next_doc()

debug_file = open("debug.txt", "a")

concepts = Counter()
count = 0
while doc is not None:
    # # for s in stok(doc):
    #     # tokens = tok(s)
    # pos_tok = pos_tag(word_tokenize(s, "russian"), lang='rus')
    # pos_tok = list(map(lambda x: (x[0], map_tag('ru-rnc','universal', x[1])), pos_tok))
    # pprint(pos_tok)
    #     # pattern = pd(tokens)
    #     # if pattern:
    #     #     print(pattern, s)
    # tokenized_sents = [list(map(lambda x: (x[0], map_tag('ru-rnc','universal', x[1])), pos_tag(word_tokenize(s, "russian", preserve_line=True), lang='rus'))) for s in sent_tokenize(doc, "russian")]

    for s in sent_tokenize(doc, "russian"):
        ts = [(token, tagger.tag_word(token)[0][1]) for token in word_tokenize(s, "russian", preserve_line=True)]
        candidates = hyp(ts)
        for c in candidates:
            debug_file.write("{}; {};\t{}\n".format(c[0], c[1], s))
            print(c)
        concepts |= Counter(candidates)

    # tokenized_sents = [[(token, tagger.tag_word(token)[0][1]) for token in word_tokenize(s, "russian", preserve_line=True)] for s in sent_tokenize(doc, "russian")]
    # for ts in tokenized_sents:
    #     candidates = hyp(ts)

    #     for c in candidates:
    #         debug_file.write("{} {}, ".format(c[0], c[1]))
    #         print(c)
    #     debug_file.write("\t")
    #     for t in ts:
    #         debug_file.write("{} ".format(t[0]))
    #     debug_file.write("\n")


    #     concepts |= Counter(candidates)
    #     # for c in candidates:
    #     #     print(c)

    
    doc = wiki.next_doc()
    # break
    count += 1
    if count % 100 == 0:
        dump_concepts(concepts)        

dump_concepts(concepts)

 

# # chunker = CRFTagger(feature_func=feature_detector)
# # chunker.set_model_file("/Volumes/External/dev/nltk-chunker-russian/russian_chunker.crf")

# news = lr.readNews()['text']
# count = 0
# while news:

#     # pos_tok = pos_tag(word_tokenize(news, "russian"), lang='rus')
#     # pos_tok = list(map(lambda x: (x[0], map_tag('ru-rnc','universal', x[1])), pos_tok))
#     # print(pos_tok)
#     # for s in stok(news):
#     #     print(s)
#     #     tokens = tok(s)
#     #     if pd(tokens):
#     #         print(news)

#     ### Grammar chunker
#     # grammar = r"""
#     #     NBAR:
#     #         {<NOUN.*|ADJ>*<NOUN.*>}  # Nouns and Adjectives, terminated with Nouns
            
#     #     NP:
#     #         {<NBAR>}
#     #         {<NBAR><ADP><NBAR>}  # Above, connected with in/of/etc...
#     #     """
#     # chunker = RegexpParser(grammar)
#     # tree = chunker.parse(pos_tok)
#     # for subtree in tree.subtrees():
#     #     if subtree.label() == 'NP': print(subtree.leaves()
#     # # print(tree)

#     # pos_tok = [pos_tag(word_tokenize(s, "russian", preserve_line=True), lang='rus') for s in sent_tokenize(news, "russian")]
#     # [print(conlltags2tree(s)) for s in tags2conll(chunker.tag_sents(pos_tok))]

#     # tokenized_sents = [list(map(lambda x: (x[0], map_tag('ru-rnc','universal', x[1])), pos_tag(word_tokenize(s, "russian", preserve_line=True), lang='rus'))) for s in sent_tokenize(news, "russian")]
#     # tokenized_sents = [pos_tag(word_tokenize(s, "russian", preserve_line=True), lang='rus') for s in sent_tokenize(news, "russian")]
#     tokenized_sents = [[(token, tagger.tag_word(token)[0][1]) for token in word_tokenize(s, "russian", preserve_line=True)] for s in sent_tokenize(news, "russian")]



#     for ts in tokenized_sents:
        
#         for c in hyp(ts):
#             # pass
#             print(c)
#         # for t in pd(ts):
#         #     print(count)
#         #     print(t)  
#         #     print()
    

#     count += 1

#     # if count == 5: break
    
#     new = lr.readNews()
#     while type(new) is dict and 'text' not in new:
#         new = lr.readNews()
#     if type(new) is not dict:
#         break
#     news = new['text']
# print(count)