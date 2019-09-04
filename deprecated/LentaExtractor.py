from LentaReader import LentaReader
import sys

# import spacy

sys.path.insert(0, "/Volumes/External/dev/")

from LanguageTools import Tokenizer, Tagger
from LanguageTools.syntaxnet_wrapper import ProcessorSyntaxNet
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




    

def noun_chunks(sentence_tree):
    np_deps = set(['nsubj', 'dobj', 'nsubjpass', 'pcomp', 'pobj', 'dative', 'appos',
              'attr', 'ROOT', 'name', 'conj'])#, 'nmod', 'amod', 'cc', ])

    pos_types = set(['NOUN', 'PROPN']) # , 'PRON', 'ADJ'

    # def check_right(i, tree):
    #     if tree[i+1].pos_ in pos_types and \
    #         tree[i+1].dep_ in np_deps and \
    #         get_noun_ans(tree[i], set()).intersection(get_noun_ans(tree[i+1], set())):
    #         return check_right(i+1, tree)
    #     else:
    #         return i+1

    def get_noun_ans(w, ans):
        if w.pos_ in pos_types:
            ans.update([w.i])
            if w.dep_ in np_deps:
                get_noun_ans(w.head_obj, ans)
        return ans

    def get_max_level(inds):
        return sorted(inds, key = lambda i: sentence_tree[i].level, reverse=True)[0]

    seen = set()

    groups = {}
    for i, word in enumerate(sentence_tree):
        if word.pos_ in pos_types and word.dep_ in np_deps:
            sn = get_max_level(get_noun_ans(sentence_tree[i], set()))
            # print(word.text, sn)
            if sn in groups:
                groups[sn].append(word.i)
            else:
                groups[sn] = [word.i]

    return groups.values()
    
    # rbracket = 0
    # lbracket = 0

    # for i, word in enumerate(sentence_tree):
    #     if i < rbracket:
    #         continue
    #     if word.pos_ in pos_types and word.dep_ in np_deps:
    #         lbracket = word.i
    #         rbracket = check_right(word.i, sentence_tree)
    #         # rbracket = word.i+1
    #         # try to extend the span to the right
    #         # to capture close apposition/measurement constructions

    #         # for rdep in sentence_tree[word.head].children:
    #         #     if rdep < word.i:
    #         #         continue
    #         #     if sentence_tree[rdep].pos_ in {'NOUN', 'PROPN'} and sentence_tree[rdep].dep_ in {'dobj','nsubj','pobj'}:
    #         #         rbracket = rdep+1
    #         if rbracket - lbracket == 1 and word.pos_ in {'CONJ', 'ADJ'}:
    #             continue
    #         yield lbracket, rbracket, 'NP'


class WordNode:
    text = ""
    i = -1
    pos_ = ""
    lemma_ = ""
    dep_ = ""
    morph_ = ""
    head = -1
    head_obj = None
    children = None
    children_ = None
    level = 0

    def __init__(self):
        self.children = []
        self.children_ = []

    def __str__(self):
        return "%s %d %s %s %d %s" % (self.text, self.i, self.pos_, self.dep_, self.head, self.children)

    def left_edge(self):
        if len(self.children) > 0:
            return self.children_[0].left_edge()
        else:
            return self.i

    


def build_tree(sentence):
    head = lambda x: x.parent
    text = lambda x: x.word_form
    pos = lambda x: x.pos_tag
    morph = lambda x: x.morph
    dep = lambda x: x.link_name

    n_tokens = len(sentence)
    tree = [WordNode() for _ in range(n_tokens + 1)]

    for ind, w in enumerate(sentence):
        tree[ind].text = text(w)
        tree[ind].i = ind
        tree[ind].pos_ = pos(w)
        tree[ind].dep_ = dep(w)
        tree[ind].morph_ = morph(w)
        tree[ind].head = head(w)
        tree[ind].head_obj = tree[head(w)]
        tree[tree[ind].head].children.append(tree[ind].i)
        tree[tree[ind].head].children_.append(tree[ind])
        tree[tree[ind].head].level += 1 if tree[tree[ind].head].level <= tree[ind].level else 0

    return tree




lentaPath = sys.argv[1]

lr = LentaReader(lentaPath)
tok = Tokenizer.Tokenizer()
tag = Tagger.Tagger()
stok = Tokenizer.PunctTokenizer()
proc = ProcessorSyntaxNet('localhost', 8111)

news = lr.readNews()['text']

for s in stok(news):
    result = proc.parse(prep_for_SN(s))
    # print_result(result)

    for s in result:
        t = build_tree(s)
        for w in t:
            print(w)

        for g in noun_chunks(t):
            print(g)
            for i in g:
                print(t[i].text, end=" ")
            print()

        # for nc in noun_chunks(t):
        #     b,e,tag = nc
        #     print(nc)
        #     for i in range(b,e):
        #         print(t[i].text, end=" ")
        #     print()
        print()
    

        


# lenta_sink = open("lenta_flat.txt", "w")

# doc_text = " ".join(news['text'].strip().split("\n"))

# counter = 0

# while news:
#     try:
#         doc_text = " ".join(news['text'].strip().split("\n"))

#         tokens = tok(doc_text)
#         f_lemmas = [l for ind, l in enumerate([tag.get_lemma(w) for w in tokens]) if tokens[ind] != l ]

#         for token in tokens:
#             lenta_sink.write("%s " % token)

#         for lemma in f_lemmas:
#             lenta_sink.write("%s " % lemma)

#         lenta_sink.write("\n")
#     except KeyboardInterrupt:
#         raise KeyboardInterrupt
#     except:
#         print(news)

#     counter += 1

#     if counter % 1000 == 0:
#         print("%d processed\r" % counter, end="")

#     news = lr.readNews()


# if __name__ == "__main__":
# lentaPath = sys.argv[2]
# spacyPath = sys.argv[1]

# nlp = spacy.load("en")
# print(nlp.pipe_names)

# nlp = spacy.load(spacyPath, disable=['parser', 'tagger'])
# nlp.add_pipe(nlp.create_pipe('sentencizer'))
# nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))

# lr = LentaReader(lentaPath)

# news = lr.readNews()




# while news:
#     # doc = nlp(news['text'])
#     try:
#         doc_text = " ".join(news['text'].strip().split("\n"))
#         doc = nlp(doc_text)

#         for token in doc:

#             if token.lemma_ == token.text:
#                 lenta_sink.write("%s " % token.text)
#             else:
#                 lenta_sink.write("%s %s " % (token.lemma_, token.text))

#         lenta_sink.write("\n")
#     except:
#         print(news)
    
#         # for token in s:
#             # print("\t", token.lemma_, token.text, token.pos_, token.tag_, token.dep_)
    
#     #     # print("\n\n")

#     news = lr.readNews()
#     # break

