# import spacy
from nltk import RegexpParser
from nltk.tag.mapping import map_tag
from nltk.chunk import tree2conlltags, conlltags2tree
from copy import copy
import pickle

import sys
sys.path.insert(0, "/Volumes/External/dev/")
from LanguageTools.CRFChunkParser import CRFChunkParser
from LanguageTools.EnsembleCRFChunker import EnsembleCRFChunker

en_keywords = set(['such', 'as', 'including', 'and', 'other', 'especially', 'or', 'and', ','])
en_patterns = [set(['such', 'as']), set(['including']), set(['and', 'other']), set(['especially'])]

ru_keywords = set(['таких', 'такие', 'такими', 'как', 'включая', 'и', 'или','другие', 'других', 'другими', 'особенно', 'в', 'частности', ','])
ru_patterns = [set(['такие', 'как']), set(['таких', 'как']), set(['такими', 'как']), set(['включая']), set(['особенно']), set(['и', 'другие']), set(['и', 'других']), set(['и', 'другими']), set(['в', 'частности'])]

pattern_descriptors = set(['P1','P2','P3','P4','P5','P6'])

pattern_map = {
    "P1": 0, # 0 means superconcept is first, -1 means last
    "P2": 0,
    "P3": 0,
    "P4": -1,
    "P5": 0,
    "P6": 0,
}

en_grammar = r"""
        NP:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        P1:
            {<NP><such><as>(<NP><,>)*(<NP><and|or>)?<NP>} 
        P2:
            {<such><NP><as>(<NP><,>)*(<NP><and|or>)?<NP>}
        P3:
            {<NP><,>?<including>(<NP><,>)*(<NP><and|or>)?<NP>}
        P4:
            {<NP>(<,><NP>)*<,>?<and><other><NP>}
        P5:
            {<NP><,>?<especially>(<NP><,>)*(<NP><and|or>)?<NP>}
        """

ru_grammar = r"""
        NP:
            {<NOUN>*<ADJ>*<NOUN.*>}#{<NOUN.*|ADJ>*<NOUN.*>}  # add NONLEX for foreign names
        P1:
            {<NP><,>?<такие|таких|такими><как>(<NP><,>)*(<NP><и|или>)?<NP>} # а так же; 
        P2:
            {<такие|таких|такими><NP><,>?<как>(<NP><,>)*(<NP><и|или>)?<NP>} #таких фильмах режиссера, как «Человек ниоткуда», «Вокзал для двоих» и «Старые клячи»
        P3:
            {<NP><,>?<включая>(<NP><,>)*(<NP><и|или>)?<NP>}
        P4:
            {<NP>(<,><NP>)*<,>?<и><другие|других|другими><NP>}
        P5:
            {<NP><,>?<особенно>(<NP><,>)*(<NP><и|или>)?<NP>} # Откуда у людей, особенно у женщин, такой менталитет?
        P6:
            {<NP><,>?<в><частности>(<NP><,>)*(<NP><и|или>)?<NP>} # kill

        # и другие, а так же другие
        """


class PatternDetector:
    def __init__(self, lang='ru'):
        if lang == 'ru':
            self.markers = ru_keywords
            self.parser = RegexpParser(ru_grammar)
            self.patterns = ru_patterns
            self.pre_parser = None
            # self.pre_parser = CRFChunkParser([], model_file="/Users/LTV/dev/LanguageTools/russian_chunker.crf")
            # self.pre_parser = pickle.load(open("/Users/LTV/dev/LanguageTools/russian_chunker.pickle", "rb"))
            self.pre_parser = EnsembleCRFChunker()
        elif lang == 'en':
            self.markers = en_keywords
            self.parser = RegexpParser(en_grammar)
            self.patterns = en_patterns
            self.pre_parser = None
        else:  
            raise NotImplementedError

    def __call__(self, tokens):
        token_copy = copy(tokens)

        token_set = set([token for token, tag in token_copy])

        if self.pre_parser:
            # token_copy = self.pre_parser.parse(token_copy, return_tree=False)
            token_copy = tree2conlltags(self.pre_parser.parse(token_copy))
            # print(token_copy)
            # print(parsed)
        
        for pattern in self.patterns:
            if len(token_set & pattern) == len(pattern):

                for ind, token_tag in enumerate(token_copy):
                    if token_tag[0].lower() in self.markers:
                        token_copy[ind] = (token_tag[0], token_tag[0].lower()) if len(token_tag) == 2 else (token_tag[0], token_tag[0].lower(), "O" if token_tag[2] not in {"B-NP", "I-NP"} else token_tag[2])
        
                if self.pre_parser:
                    tree = self.parser.parse(conlltags2tree(token_copy))
                    # print(tree)
                else:
                    tree = self.parser.parse(token_copy)
                return [s for s in tree.subtrees() if s.label() in pattern_descriptors]
        
        return []

        
if __name__=="__main__":
    from nltk import sent_tokenize, word_tokenize, pos_tag
    en_p = PatternDetector('en')
    ru_p = PatternDetector('ru')

    def en_tag(sentence):
        return pos_tag(word_tokenize(sentence, "english"), lang='eng')

    def ru_tag(sentence):
        return list(map(lambda x: (x[0], map_tag('ru-rnc','universal', x[1])), pos_tag(word_tokenize(sentence, "russian"), lang='rus')))
        # return pos_tag(word_tokenize(sentence, "russian"), lang='rus')

    print(en_p(en_tag("Beautiful Cats such as lion.")))
    print(en_p(en_tag("Cats such as lion and tiger.")))
    print(en_p(en_tag("Cats such as lion, tiger, pantera and domestic cat.")))

    print(en_p(en_tag("Such cats as lions.")))
    print(en_p(en_tag("Such cats as lions and panteras.")))
    print(en_p(en_tag("Such cats as lions, tigers and panteras.")))

    print(en_p(en_tag("Cats including lions.")))
    print(en_p(en_tag("Cats, including lions.")))
    print(en_p(en_tag("Cats including lions and panteras.")))
    print(en_p(en_tag("Cats including lions, tigers and panteras.")))

    print(en_p(en_tag("Lions and other cats.")))
    print(en_p(en_tag("Lions, tigers and other cats.")))
    print(en_p(en_tag("Lions, tigers, panteras and other cats.")))

    print(en_p(en_tag("Cats, especially lions.")))
    print(en_p(en_tag("Cats, especially lions and tigers.")))
    print(en_p(en_tag("Cats, especially lions, tigers and panteras .")))

    print(ru_p(ru_tag("Кошки такие как слоны и носороги.")))
    print(ru_p(ru_tag("Такие кошки как слоны и носороги.")))
    print(ru_p(ru_tag("Кошки, включая слонов и носорогов.")))
    print(ru_p(ru_tag("Слоны, носороги и другие кошки.")))
    print(ru_p(ru_tag("Кошки, особенно слоны и носороги.")))
    print(ru_p(ru_tag("Кошки, в частности слоны и носороги.")))
    print(ru_p(ru_tag("Что же тперь с нами будет")))
#     pos_tok = list(map(lambda x: (x[0], map_tag('ru-rnc','universal', x[1])), pos_tok))
    # en_p.parse("")