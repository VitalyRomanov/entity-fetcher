from PatternDetector import PatternDetector

from PatternDetector import ru_grammar, ru_keywords, ru_patterns
from PatternDetector import en_grammar, en_keywords, en_patterns

from PatternDetector import pattern_map

from nltk.tag.util import untag

import pymorphy2

class HyponymDetector:

    def __init__(self, lang):
        self.pattern_map = pattern_map
        self.pattern_detector = PatternDetector(lang)
        if lang == "ru":
            self._morph = pymorphy2.MorphAnalyzer()
        else:
            self._morph = None

    def _lemmatize(self, word):
        if self._morph:
            return self._morph.parse(word)[0].normal_form
        else:
            return word

    def __call__(self, sentence):
        patterns = self.pattern_detector(sentence)

        candidates = []

        for pattern in patterns:
            pos = self.pattern_map.get(pattern.label(), 1) # 1 is invalid

            if pos == 1: continue

            NPs = [sub.leaves() for sub in pattern.subtrees() if sub.label()=='NP']

            # sup_concept_cand = untag(NPs.pop(pos))
            # sup_concept = [sup_concept_cand[ind:] for ind in range(len(sup_concept_cand))]
            sup_concept = untag(NPs.pop(pos))
            sub_concept = [untag(np) for np in NPs]


            # candidates = [(" ".join(map(lambda w: self._lemmatize(w), sup)), " ".join(map(lambda w: self._lemmatize(w), sub))) for sub in sub_concept for sup in sup_concept]
            candidates = [(" ".join(sup_concept), " ".join(sub)) for sub in sub_concept]

        return candidates



