from PatternDetector import PatternDetector

from PatternDetector import ru_grammar, ru_keywords, ru_patterns
from PatternDetector import en_grammar, en_keywords, en_patterns

from PatternDetector import pattern_map

from nltk.tag.util import untag

from nltk import Tree

from PhraseNormalizer import PhraseNormalizer

# TODO
# 1. Filter terms that definitely cannot be concepts
# 2. " ".join is known to be slow

articles = set(["a", "the"])

class HyponymDetector:

    def __init__(self, lang):
        self.pattern_map = pattern_map
        self.pattern_detector = PatternDetector(lang, backend='nltk')
        self._morph = None

        self.normalize = PhraseNormalizer(lang)

        if lang == "ru":
            # import pymorphy2
            # self._morph = pymorphy2.MorphAnalyzer()
            pass
        else:
            # import spacy
            # self.spacy_nlp = spacy.load("en_core_web_md")
            pass

    def _lemmatize(self, word):
        if self._morph:
            return self._morph.parse(word)[0].normal_form
        else:
            return word

    def refine_pos_tags(self, pattern):

        # TODO
        # Need to refine POS tags for Russian language
        # can do this by looking at the POS tags for most of the
        # main nouns in the pattern and assigning the correct
        # case and number. Could be problems with this approach.
        # The most important thing here is to find the correct number {sing, plur}
        # Same probably needed to resolve compound noun chunks, although,
        # this is still a work in progress

        # can resolve the followign here as well
        # бактериальная, вирусная инфекция -> патологический процесс
        return pattern

    def __call__(self, sentence_tokens):
        patterns = self.pattern_detector(sentence_tokens)

        candidates = []

        for pattern in patterns:

            pattern = self.refine_pos_tags(pattern)
            # pos is position of the superconcept in the future list of concepts
            pos = self.pattern_map.get(pattern.label(), 1) # 1 is invalid

            if pos == 1: continue

            # for child in tree:
            #     if isinstance(child, Tree) and child.label() in pattern_descriptors:
            #         return [subchild for subchild in child if isinstance(subchild, Tree)]

            NPs = [child for child in pattern if isinstance(child, Tree)]
            # NPs = [sub.leaves() for sub in pattern.subtrees() if sub.label()=='NP']

            # def to_str(NP):
            #     return " ".join([token for token, _ in NP.leaves() if token not in articles])

            super_concept = self.generate_candidates(NPs.pop(pos), pattern.label())
            sub_concept = [self.generate_candidates(NP, pattern.label()) for NP in NPs if NP.label()[:2] == "NP"]
            fact_group = {
                "type": pattern.label(),
                "super": super_concept,
                "sub": sub_concept
            }

            if len(sub_concept) == 1:
                continue

            candidates.append(fact_group)

            # sub_concept = self.lemmatize_nps(NPs)

            # print(super_concept)

            # TODO
            # 1. Improve extraction quality by enumerating additional variants for subconcepts
            # 2. Score candidates with vector proximity or PMI
            # 3. Generate extra candidates from within single NP Done
            # 4. Remove articles DONE

            # sup_concept_cand = untag(NPs.pop(pos))
            # sup_concept = [sup_concept_cand[ind:] for ind in range(len(sup_concept_cand))]
            # sup_concept = untag(NPs.pop(pos))
            # sub_concept = [untag(np) for np in NPs]


            # candidates = [(" ".join(map(lambda w: self._lemmatize(w), sup)), " ".join(map(lambda w: self._lemmatize(w), sub))) for sub in sub_concept for sup in sup_concept]
            # candidates = [(" ".join(sup_concept).lower(), " ".join(sub).lower(), pattern.label()) for sub in sub_concept]
            # candidates = [(sup, sub, pattern.label()) for sup in super_concept for sub in sub_concept ] # <- this was the latest version
            # "P7"
            # candidates.extend(self.simple_candidates(sub for sub in pattern.subtrees() if sub.label()=='NP'))

        return candidates


    def cand_gen(self, candidate):
        return candidate
        # Candidate generation needs to be reimplemented
        # doc = self.spacy_nlp(candidate)

        # root = [token for token in doc if token.head == token][0]

        # if len(doc) > 1:
        #     full = " ".join(t.lemma_.lower() if t.head == t else t.text.lower() for t in doc)
        #     return [full, root.lemma_.lower()]
        # else:
        #     return [root.lemma_.lower()]



    def generate_candidates(self, NP, pattern_type):
        if None: #len(NP.label()) > 3 and NP.label()[:3] == "NP_": #block this branch
            candidates = []

            def candidate_iterator():
                yield " ".join([token for token, _ in NP.leaves() if token not in articles])
                for child in NP:
                    if isinstance(child, Tree):
                        yield " ".join([token for token, _ in child.leaves() if token not in articles])

            candidates = list(candidate_iterator())
            # for candidate in candidate_iterator():
            #     for candidate_lemma in self.cand_gen(candidate):
            #         if candidate_lemma not in candidates:
            #             candidates.append(candidate_lemma)

            # pre_candidates = []
            
            # pre_candidates.append(" ".join([token for token, _ in NP.leaves()]))
            # for child in NP:
            #     if isinstance(child, Tree):
            #         pre_candidates.append(
            #             " ".join(
            #                 [
            #                     token for token, _ in child.leaves()
            #                 ]
            #             )
            #         )

            # candidates = []
            # for candidate in pre_candidates:
            #     candidates.extend(self.cand_gen(candidate))

        else:

            #### candidates = self.cand_gen(" ".join([token for token, _ in NP.leaves() if token not in articles]))
            # candidates = [" ".join([token for token, _ in NP.leaves() if token not in articles])]
            candidates = {
                "type": NP.label(),
                "candidates": [" ".join(self.normalize([token for token, _ in NP.leaves() if token not in articles], NP.label()))]
            }

        # candidates = [" ".join(self.normalize(candidate.split())) for candidate in candidates]

        return candidates

    def lemmatize_nps(self, NPs):
        return [
            " ".join(
                [
                    t.lemma_.lower() if t.head == t else t.text.lower() for t in self.spacy_nlp(" ".join(
                        [
                            token for token, _ in NP.leaves() if token not in articles
                        ]
                    ))
                ]
            ) for NP in NPs]

    def simple_candidates(self, NPs):
        # candidates = []
        for NP in NPs:
            candidate = self.cand_gen(" ".join([token for token, _ in NP.leaves() if token not in articles]))
            # cand_gen can generate only one candidate if the concept sonsists of one word
            if len(candidate) != 2:
                continue
            yield (candidate[1], candidate[0], 'P7')
            # candidates.append(tuple(candidate))
        # return candidates






if __name__ == "__main__":
    hyp = HyponymDetector("en")

    from pprint import pprint

    [pprint(hyp(s)) for s in
     """The research will also include the Engineering, the Law School, School of Information, and other colleges or programs.
     Additional methods for fiat deposits, including credit cards, as well as wire and bank transfers, will be added in the near future.
     Institutionalization is the at-scale participation in the crypto market of banks, broker dealers, exchanges, payment providers, fintechs, and other entities in the global financial services ecosystem.""".split("\n")]

    hyp_ru = HyponymDetector("ru")

    [pprint(hyp_ru(s)) for s in
    """Северо-восток Сибири и Дальний Восток — регионы преобладания средневысотных горных хребтов, таких как Сихотэ-Алинь, Верхоянский, Черского и т. д. Полуостров Камчатка (здесь находится самый высокий вулкан Евразии Ключевская Сопка (4750 м) и Курильские острова на крайнем востоке — территория вулканов.
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
    Многие школы соционики утверждают о неполном соответствии типологии Майерс-Бриггс и соционической типологии, однако считают допустимым использование различных дихотомических тестов, включая различные адаптированные версии опросника Майерс-Бриггс, в качестве одного из инструментов, наряду с другими, для определения соционического типа.""".split("\n")]
    # pprint(hyp_ru("Кошки такие как слоны и носороги."))
    # pprint(hyp_ru("Кошки, в частности слоны и носороги."))
    # pprint(hyp_ru("Кошки такие как слоны и носороги."))
    # pprint(hyp_ru("Кошки такие как слоны и носороги."))

    
