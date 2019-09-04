from collections import Counter
import sys
from pprint import pprint
import spacy

data_path = sys.argv[1]

spacy_nlp = spacy.load("en_core_web_md")

def read_pairs():
    for line in open(data_path).read().strip().split("\n"):
        yield tuple(line.split("\t")[:2])

super_c, sub_c = zip(*read_pairs())

super_c = set(super_c)
# sub_c = set(sub_c)

# print("Total super_c: ", len(super_c))
# print("Total sub_c: ", len(sub_c))

# only_sub = sub_c - super_c
# concepts = super_c | sub_c - only_sub

# print("Total leafs: ", len(only_sub))
# print("Total concepts: ", len(concepts))

# pprint(only_sub)

def cand_gen(candidate):
    doc = spacy_nlp(candidate)

    root = [token for token in doc if token.head == token][0]

    if len(doc) > 1:
        full = " ".join(t.lemma_.lower() if t.head == t else t.text.lower() for t in doc)
        return [root.lemma_.lower(), full]
    else:
        return []

with open("super_c_generatization.txt", "w") as scg:
    for c in super_c:
        candidates = cand_gen(c)
        if candidates:
            scg.write("%s\t%s\n" % (candidates[0], candidates[1]))