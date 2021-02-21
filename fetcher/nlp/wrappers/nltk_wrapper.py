import logging
from typing import List, Set, Tuple
from nltk.tokenize import word_tokenize
from nltk.data import load
from nltk.tag import _get_tagger, _pos_tag

from nltk import RegexpParser
from nltk import RegexpTokenizer
from nltk.chunk import tree2conlltags
import pymorphy2



from copy import copy

# from PatternDetector import en_keywords, ru_keywords

class NpEnExceptions:
    help_avoiding_NP = {'Dr', 'dr', 'kind', 'of', 'etc'}
    exceptions_ = {"which", "thing", "many", "several", "few", "multiple", "all", "“", "”", "alike", "’", "–", "—",
                  "overall", "this", "‘"}
    keywords = help_avoiding_NP | exceptions_

class NpRuExceptions:
    help_avoiding_NP = {'на', 'качестве', 'том', 'числе', 'под', 'руководством', 'т.', 'д.', 'п.'}
    exceptions_ = {"различные", "различных", "различным", "различными"}
    keywords = help_avoiding_NP | exceptions_


key_tokens = set(["'s", "of", "in", "with", "for", "on", "over", "throughout"])
key_tokens.update(en_keywords)
key_tokens.update(ru_keywords)
key_tokens.update(never_part_of_NP)
key_tokens.update(never_part_of_NP_ru)
key_tokens.update(help_avoiding_NP_ru)
key_tokens.update(help_avoiding_NP_en)


# TODO:
# 3. names do not seem to parse
# 4. and NP does not process 100% of the time
# 6. Such thing, or no such thing are two antipatterns
# 7. Incorporate numerals
#       In addition to relatively young projects, a number of major exchanges have made their choice in favor of Malta, including Binance, OKEx, ZB.com, as well as such famous blockchain projects as TRON, Big One, Cubits, Bitpay and others.
# 8. Antipatterns





def process_apostrof_s(tokens: List[str]) -> List[str]:
    """
    Merges ["[`|'|‘]","s"] into a single token
    :param tokens: list of tokens
    :return: list of tokens with matching tokens merged
    """
    locations = []
    for ind, token in enumerate(tokens):
        if ind == len(tokens) - 1:
            continue

        if (token == "`" or token == "’" or token == "‘" or token == "'") and tokens[ind + 1] == "s":
            locations.append(ind)

    while locations:
        c_loc = locations.pop(-1)
        tokens.pop(c_loc)
        tokens.pop(c_loc)
        tokens.insert(c_loc, "'s")

    return tokens


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

class NltkWrapper:
    def __init__(self, language):
        self.lang_code = language

        if language == 'en':
            self.lang_name = 'english'
            self.tagger_lang = 'eng'
            grammar = None
        elif language == 'ru':
            self.lang_name = 'russian'
            self.tagger_lang = 'rus'
            grammar = None
            self.morph_expander = RuMorphologyExpander()
        else:
            raise NotImplemented(f"Language '{language}' is not supported")

        # Load NLTK models
        self.sent_tokenizer = load('tokenizers/punkt/{0}.pickle'.format(self.lang_name))
        self.tagger = _get_tagger(self.tagger_lang)
        # Load grammar parser
        self.create_noun_chunk_grammar_parser(grammar)

        self.tokenizer = RegexpTokenizer(
            # "[a-z]+[:.].*?(?=\s)|[A-Za-zА-Яа-яё]\.|[A-Za-zА-Яа-яё][A-Za-zА-Яа-яё-]*|[^\w\s]|[0-9]+"
            # "[A-Za-zА-Яа-яё]\.|[A-Za-zА-Яа-яё]+-[A-Za-zА-Яа-яё]+|[A-Za-zА-Яа-яё]+|[^\w\s]|[0-9]+"
            "\w\.|\w+-\w+|\w+|[^\w\s]|[0-9]+"
        )

    def init_noun_chunk(self, grammar):
        if grammar is not None:
            self.noun_chunk_parser = RegexpParser(grammar)
        else:
            self.noun_chunk_parser = None

    def create_grammar_parser(self, grammars):
        if grammars is not None:
            self.grammar_parsers = [RegexpParser(grammar) for grammar in grammars]
        else:
            self.grammar_parsers = None

    def parse_with_grammars(self, token_tags):
        # add special proprocessing here
        # for ind, tag in enumerate(tags):
        #     if tag[0].lower() in key_tokens:
        #         tags[ind] = (tags[ind][0], tags[ind][1] + "_" + tags[ind][0].lower())

        parsed = token_tags
        for parser in self.grammar_parsers:
            parsed = parser.parse(parsed)

        return parsed

    def sentencize(self, text):
        return self.sent_tokenizer.tokenize(text)

    def tokenize(self, sentence):
        tokens = self.tokenizer.tokenize(sentence)
        tokens = process_apostrof_s(tokens)
        return tokens

    def tag(self, tokens, tagset='universal'):
        tags = _pos_tag(tokens, tagset, self.tagger, self.tagger_lang)
        tags = simple_pos_fix(tags)  # hot fix for some punctuation being labeled incorrectly
        if self.lang_code == "ru":
            tags = self.morph_expander(tags)
        return tags

    def __call__(self, text):
        sents = self.sentencize(text)
        t_sents = [self.tokenize(sent) for sent in sents]
        tags = [self.tag(t_sent) for t_sent in t_sents]
        return tags

    def noun_chunks(self, text=None, tokens=None, parse_chunks=True):
        if tokens is None:
            tokens = self.tokenize(text)
        tags = self.tag(tokens)

        if parse_chunks:
            if self.noun_chunk_parser is not None:
                tags = self.noun_chunk_parser.parse(tags)
            else:
                logging.warning("Chunker grammar is not defined")
        return tags

    def parse_with_grammars(self, text=None, tokens=None):
        if tokens is None:
            tokens = self.noun_chunks(text)






if __name__ == "__main__":
    from pprint import pprint

    nlp_en = NltkWrapper("en")
    text_en = """
    Alice`s Adventures in Wonderland (commonly shortened to Alice in Wonderland) is an 1865 novel written by English author Charles Lutwidge Dodgson under the pseudonym Lewis Carroll.[1] It tells of a young girl named Alice falling through a rabbit hole into a fantasy world populated by peculiar, anthropomorphic creatures.
    The kind of societal change Dr Ammous predicts in his book, and spoke about with their reporter, severely threatens a status quo, which such mainstream publications such as The Express is usually keen to uphold.
    This particular stream saw members of the community such as Bitcoin.com’s Roger Ver, Ethereum’s Vitalik Buterin who briefly visited, Andreas Brekken of Shitcoin.com, and many more special guests.
    With regard to Dai itself, stablecoin sceptics such as Preston Byrne often point out that the token is overcollateralized to ETH, so that creating $1 worth of Dai will take >$1 worth of ETH.
    Its major dominance is in the Asian market especially South Korea, Singapore, and Japan.
    The research will also include the Engineering, the Law School, School of Information, and other colleges or programs.
    Once launched, Huobi Chain will offer users a variety of benefits, including security, transparency, fast, scalability, and smart contract capability.
    """
    # tags_en = nlp_en(text_en)
    # tags_en = nlp_en.noun_chunks(text_en)
    # tags_en.pprint()
    #
    # seen = []
    #
    # # print(tags_en.treepositions())
    #
    # from nltk import Tree
    # for child in tags_en:
    #     if isinstance(child, Tree):
    #         if len(child.label()) > 3 and child.label()[:3] == "NP_":
    #             for c in child:
    #                 print("\t", c)
    #     else:
    #         print(child)

    # print(child)

    # for tree in tags_en.subtrees():
    #     if tree.label == "S":
    #         pass
    #     else:
    #         if len(tree.label()) > 3 and tree.label()[:3] == "NP_":
    #             nested = []
    #             nested.append(" ".join([tok for tok, _ in tree.leaves()]))
    #             print(nested)

    # nested.append([t for t in tree.subtrees() if t.label() == "NP"])

    # all_trees = [tree for tree in tags_en.subtrees() if tree not in nested]

    # for tree in all_trees:

    #     # for t in tree:
    #     tree.pprint()
    #     # print(list(tree.subtrees()))

    #     print("\n\n\n")
    # pprint(tags_en)

    nlp_ru = NltkWrapper("ru")
    text_ru = "«Приключения Алисы в Стране чудес» (англ. Alice’s Adventures in Wonderland), часто используется сокращённый вариант «Алиса в Стране чудес» (англ. Alice in Wonderland) — сказка, написанная английским математиком, поэтом и прозаиком Чарльзом Лютвиджем Доджсоном под псевдонимом Льюис Кэрролл и изданная в 1865 году. В ней рассказывается о девочке по имени Алиса, которая попадает сквозь кроличью нору в воображаемый мир, населённый странными антропоморфными существами."
    text_ru = """
    Северо-восток Сибири и Дальний Восток — регионы преобладания средневысотных горных хребтов, таких как Сихотэ-Алинь, Верхоянский, Черского и т. д. Полуостров Камчатка (здесь находится самый высокий вулкан Евразии Ключевская Сопка (4750 м) и Курильские острова на крайнем востоке — территория вулканов.
    Помимо деления на ландшафтные зоны, существует деление на физико-географические сектора, которые различаются атмосферной циркуляцией, континентальностью климата и другими характеристиками.
    По общему согласию государств-участников СНГ было решено рассматривать Российскую Федерацию в качестве государства-продолжателя СССР со всеми вытекающими из этого последствиями, включая переход к Российской Федерации места постоянного члена Совета Безопасности ООН и признание за Российской Федерацией статуса ядерной державы по смыслу Договора о нераспространении ядерного оружия 1968 года.
    Правительством Ельцина — Гайдара были проведены либерализация розничных цен, либерализация внешней торговли, реорганизация налоговой системы и другие преобразования, радикально изменившие экономическую ситуацию в стране.
    Является членом значительного числа других международных организаций, включая Совет Европы и ОБСЕ.
    С российским загранпаспортом можно въехать без визы в 76 государств мира, в 32 государствах можно получить визу автоматически по прибытии, в остальные государства, в том числе в страны Евросоюза, США, Канаду, Великобританию, Китай, Японию и другие страны въездную визу необходимо получать заблаговременно.
    В последние годы по объёму ВДС в обрабатывающей промышленности Россия обошла такие страны, как Испания, Канада, Мексика, Индонезия (эти страны опережали Россию по состоянию на 2002 год).
    В Северном районе к основным отраслям относятся добыча угля, нефти, газа, апатитов, никеля и других металлов, а также заготовка леса и ловля рыбы.
    Русские расселены по территории страны неравномерно: в некоторых регионах, таких как Чечня, составляют менее 2 % населения.
    Конституция гарантирует «свободу совести, свободу вероисповедания, включая право исповедовать индивидуально или совместно с другими любую религию или не исповедовать никакой, свободно выбирать, иметь и распространять религиозные и иные убеждения и действовать в соответствии с ними».
    Благодаря созданным научным школам под руководством Курчатова, Королёва и других учёных в СССР было создано ядерное оружие и космонавтика.
    Представителями русского балета, достигшими мировой славы были такие выдающиеся танцовщики как Матильда Кшесинская, Ольга Спесивцева, Вацлав Нижинский, Анна Павлова, Тамара Карсавина, Джордж Баланчин, положивший начало американскому балету и современному неоклассическому балетному искусству в целом; Марис Лиепа, Галина Уланова, Константин Сергеев, Майя Плисецкая.
    В Таймырском Долгано-Ненецком районе Красноярского края, в бассейне Нижней Таймыры есть такие объекты как Река Мамонта (названа так в честь находки на ней в 1948 году скелета Таймырского мамонта), Левый Мамонт и озеро Мамонта.
    Согласно Блутнеру и Хохнаделю, соционика в основном используется в России и странах Восточной Европы, а несколько похожая на неё постъюнговская типология Майерс — Бриггс используется больше в США и Западной Европе, при этом соционика имеет ряд отличий от типологии Майерс — Бриггс, включая наличие теории взаимодействий или отношений между типами.
    Многие школы соционики утверждают о неполном соответствии типологии Майерс-Бриггс и соционической типологии, однако считают допустимым использование различных дихотомических тестов, включая различные адаптированные версии опросника Майерс-Бриггс, в качестве одного из инструментов, наряду с другими, для определения соционического типа.
    """
    tags_ru = nlp_ru(text_ru)
    tags_ru = nlp_ru.noun_chunks(text_ru)
    print(tags_ru)
