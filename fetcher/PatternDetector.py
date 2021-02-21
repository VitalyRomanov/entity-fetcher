# import spacy
from typing import List, Tuple

import pymorphy2
from nltk import RegexpParser
from nltk.tag.mapping import map_tag
from nltk.chunk import tree2conlltags, conlltags2tree
from nltk import Tree
from copy import copy
import pickle

from pprint import pprint

from LanguageTools.wrappers.nltk_wrapper import NltkWrapper, GrammarParser, NpEnExceptions, NpRuExceptions
from fetcher.nlp.grammars import *


class EnPatterns:
    keywords = {'such', 'as', 'including', 'and', 'other', 'especially', 'or', 'and', ',', "well"} | NpEnExceptions.keywords
    patterns = [{'such', 'as'}, {'including'}, {'and', 'other'}, {'especially'}]


class RuPatterns:
    extra_ru_keywords = {
        "самый", "самого", "самому", "самым", "самом", "самая", "самой", "самую", "самое", "самые",
        "самых", "самым", "самыми"
    }
    keywords = {'таких', 'такие', 'такими', 'как', 'включая', 'и', 'или', 'другие', 'других', 'другими', 'особенно',
                'в', 'частности', ','} | NpRuExceptions.keywords | extra_ru_keywords
    patterns = [{'такие', 'как'}, {'таких', 'как'}, {'такими', 'как'}, {'таким', 'как'},
                {'включая'}, {'особенно'}, {'и', 'другие'}, {'и', 'других'}, {'и', 'другими'},
                {'и', 'другим'}, {'в', 'частности'}]


class PatternDescriptors:
    descriptors = {'P1', 'P1_nomn', 'P1_gent_accs_loct', 'P1_datv', 'P1_ablt', 'P2', 'P3', 'P4', 'P4_nomn',
                   'P4_gent_accs_loct', 'P4_datv', 'P4_ablt', 'P5', 'P6'}

    map = {
        "P1": 0,  # 0 means superconcept is first, -1 means last
        "P1_nomn": 0,
        "P1_gent_accs_loct": 0,
        "P1_datv": 0,
        "P1_ablt": 0,
        "P2": 0,
        "P3": 0,
        "P4": -1,
        "P4_nomn": -1,
        "P4_gent_accs_loct": -1,
        "P4_datv": -1,
        "P4_ablt": -1,
        "P5": 0,
        "P6": 0,
    }


class HearstPatternGrammarParser(GrammarParser):
    def __init__(self, lang):
        super(HearstPatternGrammarParser, self).__init__(lang)

    def _get_grammar(self, lang):
        if lang == "en":
            return HearstNpEnGrammar.grammar + HearstEnPatterns.grammar
        elif lang == "ru":
            return HearstNpRuGrammar.grammar + HearstRuPatterns.grammar
        else:
            raise NotImplementedError(f"Language is not supported: {lang}")

    def _set_exception_set(self):
        self._exceptions = EnPatterns.keywords | RuPatterns.keywords


from LanguageTools.wrappers.nltk_wrapper import NltkWrapper


class RuMorphologyExpander:
    pos_for_expansion = {'NOUN', 'ADJ'}

    def __init__(self):
        self.morph_analyzer = pymorphy2.MorphAnalyzer()

    def morph_pos_ru(self, token: str):
        """
        Perform morphological alalysis for a token in russian language
        :param token:
        :param analyzer:
        :return:
        """
        token, pos = token
        p = self.morph_analyzer.parse(token)[0]
        gend = p.tag.gender if p.tag.gender else "None"
        return f"{pos}_{p.tag.case}_{gend}_{p.tag.number}"

    def __call__(self, sent: List[Tuple[str, str]]):
        """
        Replace pos tags that occur in RU_POS_FOR_EXPANSION with
        their morphologically enriched versions.
        :param sent: POS-tagged tokens in NLTK format
        :param analyzer:
        :return:
        """
        for ind in range(len(sent)):
            token, pos = sent[ind]
            if pos in self.pos_for_expansion:
                sent[ind] = (token, self.morph_pos_ru(sent[ind]))

        return sent


class CharSets:
    punkt = set("[-!\"#$%&'()*+,/:;<=>?@[\]^_`{|}~—»«“”„….]")

def simple_pos_fix(tags):
    for ind, tag in enumerate(tags):
        if len(tag[0]) == 1 and tag[0] in CharSets.punkt:
            if tag[1] != ".":
                tags[ind] = (tag[0], ".")
    return tags


class PatternPipeline(NltkWrapper):
    def __init__(self, lang):
        super(PatternPipeline, self).__init__(lang)
        if lang == "ru":
            self.morph_expander = RuMorphologyExpander()

    def set_grammar_parser(self, lang):
        self.grammar_parser = HearstPatternGrammarParser(lang)

    def tag(self, tokens, tagset='universal'):
        tags = self.tagger(tokens, tagset=tagset)
        tags = simple_pos_fix(tags)  # hot fix for some punctuation being labeled incorrectly
        if self.lang_code == "ru":
            tags = self.morph_expander(tags)
        return tags


class PatternDetector:
    def __init__(self, lang, backend="nltk"):
        lang = lang.lower()
        if lang in {'rus', "ru", "russian", ''}:
            lang = 'ru'
        elif lang in {'eng', 'en', 'english'}:
            lang = 'en'
        else:
            raise NotImplementedError(f"Language is not supported: {lang}")

        self.pre_parser = None

        if lang == 'ru':
            self.markers = RuPatterns.keywords
            self.patterns = RuPatterns.patterns
        elif lang == 'en':
            self.markers = EnPatterns.keywords
            self.patterns = EnPatterns.patterns

        self.grammar_parsers = HearstPatternGrammarParser(lang)

        if lang == 'ru':
            self.pre_parser = None
        elif lang == 'en':
            pass
        else:
            raise NotImplementedError()

        self.nlp = PatternPipeline(lang)

    def __call__(self, sentence_text):
        tokens = self.nlp.tokenize(sentence_text)

        token_set = set(t.lower() for t in tokens)

        for pattern in self.patterns:
            # if all words from the pattern occur in the sentence
            if len(token_set & pattern) == len(pattern):
                token_tags = self.nlp.tag(tokens)
                tree = self.nlp.parse_grammar(token_tags)

                return [s for s in tree.subtrees() if s.label() in PatternDescriptors.descriptors]

        return []


