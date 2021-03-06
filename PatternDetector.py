# import spacy
from nltk import RegexpParser
from nltk.tag.mapping import map_tag
from nltk.chunk import tree2conlltags, conlltags2tree
from nltk import Tree
from copy import copy
import pickle

from pprint import pprint
from nltk import RegexpTokenizer

import sys

en_keywords = set(['such', 'as', 'including', 'and', 'other', 'especially', 'or', 'and', ','])
en_patterns = [set(['such', 'as']), set(['including']), set(['and', 'other']), set(['especially'])]

ru_keywords = set(
    ['таких', 'такие', 'такими', 'как', 'включая', 'и', 'или', 'другие', 'других', 'другими', 'особенно', 'в',
     'частности', ','])
ru_patterns = [set(['такие', 'как']), set(['таких', 'как']), set(['такими', 'как']), set(['таким', 'как']),
               set(['включая']), set(['особенно']), set(['и', 'другие']), set(['и', 'других']), set(['и', 'другими']),
               set(['и', 'другим']), set(['в', 'частности'])]

extra_ru_keywords = [
    "самый",
    "самого",
    "самому",
    "самым",
    "самом",
    "самая",
    "самой",
    "самую",
    "самое",
    "самые",
    "самых",
    "самым",
    "самыми"
]

ru_keywords.update(extra_ru_keywords)

pattern_descriptors = set(
    ['P1', 'P1_nomn', 'P1_gent_accs_loct', 'P1_datv', 'P1_ablt', 'P2', 'P3', 'P4', 'P4_nomn', 'P4_gent_accs_loct',
     'P4_datv', 'P4_ablt', 'P5', 'P6'])

pattern_map = {
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

en_grammar = r"""
        NP:
            {<DT>?<JJ>*<NN.*>}
        NP:
            {<U-NP>}
        NP:
            {<B-NP>(<I-NP>)*<L-NP>?}
            # {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        NP:
            {(<I-NP>)*<L-NP>?}
        NP:
            {<L-NP>}
        NP:
            {<I-NP>}
        P1:
            {<NP.*><.*_such><.*_as>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_or>)?<NP.*>}
        P1:
            {<NP.*><SRV_such_as>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_or>)?<NP.*>}
        P2:
            {<.*_such><NP.*><.*_as>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_or>)?<NP.*>}
        P3:
            {<NP.*><.*_,>?<.*_including>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_or>)?<NP.*>}
        P4:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<.*_and><.*_other><NP.*>}
        P4:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_and_other><NP.*>}
        P5:
            {<NP.*><.*_,>?<.*_especially>(<NP.*><.*_,>)*(<NP.*><.*_and|.*_Por>)?<NP.*>}
        """
# TODO:
# 1. Pattern 1: NP such as NP and NP, NP, NP and NP, where first NP and NP is actually one NP
#     After the Forum completed its basic standard reference architecture, as of May 2018, it reportedly completed ten international blockchain standards such as terminology and concepts, reference architecture, classification and ontology, which have now entered development stage.
#     Some sources familiar with the matter believed that cancellation of the planned ICO can be a result of increasingly strict regulations that are proposed by such entities as the Securities and Exchange Commission, Commodity Futures Trading Commission, and others since the company initially began examining a possibility to launch its ICO.
# 2. Pattern 1: Sometimes tail of pattern 1 is an auxiliary sentence
#     However, over the past six months, as he has learnt more about Ripple and XRP (perhaps, partly due to conversations with Ripple employees, such as CTO David Schwartz, and famous XRP fans such as Michael Arrington, the co-founder of digital asset management firm Arrington XRP Capital), hate seems to have gradually turned into love.
# 3. Pattern 2: Create grammar pattern for no such so that it does not participate in target patterns
# 4. Pattern 2: filter "such a", because it has different meaning
# 5. Pattern 2: does not always work. Maybe need to try classifying before parsing
#       The law requires that salaried workers who earn a minimum of 200,000 yen from cryptocurrency trading and investing annually to declare such earnings as income
#       It’s fair to describe such behavior as a bet, as no one can predict where the market is going, but if you’re experienced and have insight into crypto movements, futures could prove indispensable.
#       Explaining how the privacy-focused capabilities of Zcash will be supported on Coinbase, the company revealed that it would offer partial support for shielded transactions until such a time as local regulations allow for full implementation of transaction shielding.
#       The move to open source the code indicates that Bitmain may not necessarily be offering such services as part of its core business model moving forward.
#       They declared all such fundraising-related activities as illegal.
# 6. Patter 3: Does not always work
#       In addition to this, the binaries are available in many options including Solaris, Plan 9, and BSD operating systems.
#       Since the acrimonious fork, a lot has happened within the BCH ecosystem including a few exchanges listing both chains as separate coins.
#       Kraken has warned customers that the SV chain does not meet the company’s traditional listing requirements for a variety of reasons including the fact that it has “no known wallets supporting replay protection, miners are operating at a loss, and representatives threatening and openly hostile toward other chains.” Additionally, the exchange said it has completed only a small amount of code review and stressed that “large holders have indicated they’d be dumping everything.”
#       Ping An Bank is undergoing a series of business changes under the auspices of financial technology, including the use of artificial intelligence (AI), big data, blockchain, and cloud computing in order to “ensure low-cost, efficient and personalized public services,” the People’s Daily reports.
# 7. Patter 4: Does not always work
#       Also, keep up with your holdings, BCH and other coins, on our market charts at Satoshi’s Pulse, another original and free service from Bitcoin.com.
#       Mir, an international broadcasting corporation with several Russian language TV channels, a radio station and an online outlet, is launching a new program that will inform viewers about digital coins, mining and other related technologies.
#       Based on current market conditions and the intensity of the drop over the last 24 to 48 hours, Bitcoin Cash and other major cryptocurrencies are expected to drop further in price, with BCHABC eyeing a test of $180 for the first time in its 15-month history.
#       According to a letter released by the Institute for Business and Social Impact (IBSI), which is to work with the Masters of Financial Engineering (MFE) program at Berkeley, dictates that the grant will finance the faculty, student research and other related activities across the Berkeley Campus.
# 8. Pattern 5: Some bugs: did not parse last entity
#       Its major dominance is in the Asian market especially South Korea, Singapore, and Japan.
# 9. When having composed NP (NP in NP and such) most of the time we need to select only one NP as target concept
#       It is pretty impossible to do this with grammars, e.g. 'payments for major companies such as google'
#       Can try to resolve this using word vectors. What is the concept that is the closest to all subconcepts
#       For some it is easy to decide: forms of capital -> equity
# 11. Exclude 'and other'


ru_grammar = r"""
        NP:
            {<NOUN>*<ADJ>*<NOUN.*>}#{<NOUN.*|ADJ>*<NOUN.*>}  # add NONLEX for foreign names
        NP:
            {<U-NP>}
        NP:
            {<B-NP>(<I-NP>)*<L-NP>?}
        NP:
            {(<I-NP>)*<L-NP>?}
        NP:
            {<L-NP>}
        NP:
            {<I-NP>}
        P1:
            {<NP.*><.*_,>?<.*_такие|.*_таких|.*_такими><.*_как>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} # а так же;
        P1_nomn:
            {<NP.*><.*_,>?<SRV_takie_kak>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>}
        P1_gent_accs_loct:
            {<NP.*><.*_,>?<SRV_takih_kak>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>}
        P1_datv:
            {<NP.*><.*_,>?<SRV_takim_kak>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>}
        P1_ablt:
            {<NP.*><.*_,>?<SRV_takimi_kak>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} 
        P2:
            {<.*_такие|.*_таких|.*_такими><NP.*><.*_,>?<.*_как>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} #таких фильмах режиссера, как «Человек ниоткуда», «Вокзал для двоих» и «Старые клячи»
        P3:
            {<NP.*><.*_,>?<.*_включая>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>}
        P4:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<.*_и><.*_другие|.*_других|.*_другими><NP.*>}
        P4_nomn:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_i_drygiye><NP.*>}
        P4_gent_accs_loct:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_i_drygih><NP.*>}
        P4_datv:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_i_drygim><NP.*>}
        P4_ablt:
            {<NP.*>(<.*_,><NP.*>)*<.*_,>?<SRV_i_drygimi><NP.*>}
        P5:
            {<NP.*><.*_,>?<.*_особенно>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} # Откуда у людей, особенно у женщин, такой менталитет?
        P6:
            {<NP.*><.*_,>?<.*_в><.*_частности>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} # kill
        P6:
            {<NP.*><.*_,>?<SRV_v_chasnosti>(<NP.*><.*_,>)*(<NP.*><.*_и|.*_или>)?<NP.*>} # kill

        # и другие, а так же другие
        """


# TODO
# 1. This sentence will generate incorrect candidates
#       В Северном районе к основным отраслям относятся добыча угля, нефти, газа, апатитов, никеля и других металлов, а также заготовка леса и ловля рыбы.
#       Конституция гарантирует «свободу совести, свободу вероисповедания, включая право исповедовать индивидуально или совместно с другими любую религию или не исповедовать никакой, свободно выбирать, иметь и распространять религиозные и иные убеждения и действовать в соответствии с ними».


class PatternDetector:
    def __init__(self, lang='ru', backend=None):

        self.pre_parser = None
        self.tokenizer = RegexpTokenizer(
            "[A-Za-zА-Яа-яё]\.|[A-Za-zА-Яа-яё][A-Za-zА-Яа-яё-]*|[^\w\s]|[0-9]+"
        )

        if lang == 'ru':
            self.markers = ru_keywords
            self.patterns = ru_patterns
            self.parser = RegexpParser(ru_grammar)
        elif lang == 'en':
            self.markers = en_keywords
            self.patterns = en_patterns
            self.parser = RegexpParser(en_grammar)
            # import spacy
            # self.spacy_nlp = spacy.load("en_core_web_md")

        if backend == 'spacy':
            from spacy_wrapper import SpacyWrapper
            self.nlp = SpacyWrapper(lang)
        elif backend == "nltk":
            if lang == 'ru':
                self.pre_parser = None
            elif lang == 'en':
                pass
            else:
                raise NotImplementedError()

            from nltk_wrapper import NltkWrapper
            self.nlp = NltkWrapper(lang)
        else:
            raise NotImplementedError("Unsupported backend: %s" % backend)

    def __call__(self, sentence_text):
        tokens = self.tokenizer.tokenize(sentence_text.lower())

        token_set = set(tokens)

        for pattern in self.patterns:
            # if all words from the pattern occur in the sentence
            if len(token_set & pattern) == len(pattern):

                token_tags = self.nlp.noun_chunks(sentence_text)

                # Process special markers
                # Currently processed in nltk_wrapper
                # for (ind, (token_tag)) in enumerate(token_tags):
                #     if token_tag[0].lower() in self.markers:
                #         token_tags[ind] = (token_tag[0], token_tag[0].lower()) if len(token_tag) == 2 else \
                #             (token_tag[0], token_tag[0].lower(), "O" if token_tag[2] not in {"B-NP", "I-NP"} else token_tag[2])

                if self.pre_parser:
                    tree = self.parser.parse(conlltags2tree(token_tags))
                else:
                    tree = self.parser.parse(token_tags)

                return [s for s in tree.subtrees() if s.label() in pattern_descriptors]

        return []


