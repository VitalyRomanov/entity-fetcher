from fetcher.HyponymExtractor import HyponymDetector
from pprint import pprint
import pytest

def get_super(pattern):
    return pattern['super']['candidates']

def get_sub(pattern):
    cand = []
    for c in pattern['sub']:
        cand += c['candidates']
    return cand

def simplify(pattern):
    if pattern:
        return [pattern[0]['type'], get_super(pattern[0]), get_sub(pattern[0])]
    else:
        return []

en_test_sents = """The research will also include the Engineering, the Law School, School of Information, and other colleges or programs.
Additional methods for fiat deposits, including credit cards, as well as wire and bank transfers, will be added in the near future.
Institutionalization is the at-scale participation in the crypto market of banks, broker dealers, exchanges, payment providers, fintechs, and other entities in the global financial services ecosystem.
After the Forum completed its basic standard reference architecture, as of May 2018, it reportedly completed ten international blockchain standards such as terminology and concepts, reference architecture, classification and ontology, which have now entered development stage.
Some sources familiar with the matter believed that cancellation of the planned ICO can be a result of increasingly strict regulations that are proposed by such entities as the Securities and Exchange Commission, Commodity Futures Trading Commission, and others since the company initially began examining a possibility to launch its ICO.
However, over the past six months, as he has learnt more about Ripple and XRP (perhaps, partly due to conversations with Ripple employees, such as CTO David Schwartz, and famous XRP fans such as Michael Arrington, the co-founder of digital asset management firm Arrington XRP Capital), hate seems to have gradually turned into love.
The law requires that salaried workers who earn a minimum of 200,000 yen from cryptocurrency trading and investing annually to declare such earnings as income
It’s fair to describe such behavior as a bet, as no one can predict where the market is going, but if you’re experienced and have insight into crypto movements, futures could prove indispensable.
Explaining how the privacy-focused capabilities of Zcash will be supported on Coinbase, the company revealed that it would offer partial support for shielded transactions until such a time as local regulations allow for full implementation of transaction shielding.
The move to open source the code indicates that Bitmain may not necessarily be offering such services as part of its core business model moving forward.
They declared all such fundraising-related activities as illegal.
In addition to this, the binaries are available in many options including Solaris, Plan 9, and BSD operating systems.
Since the acrimonious fork, a lot has happened within the BCH ecosystem including a few exchanges listing both chains as separate coins.
Kraken has warned customers that the SV chain does not meet the company’s traditional listing requirements for a variety of reasons including the fact that it has “no known wallets supporting replay protection, miners are operating at a loss, and representatives threatening and openly hostile toward other chains.” Additionally, the exchange said it has completed only a small amount of code review and stressed that “large holders have indicated they’d be dumping everything.”
Ping An Bank is undergoing a series of business changes under the auspices of financial technology, including the use of artificial intelligence (AI), big data, blockchain, and cloud computing in order to “ensure low-cost, efficient and personalized public services,” the People’s Daily reports.
Also, keep up with your holdings, BCH and other coins, on our market charts at Satoshi’s Pulse, another original and free service from Bitcoin.com.
Mir, an international broadcasting corporation with several Russian language TV channels, a radio station and an online outlet, is launching a new program that will inform viewers about digital coins, mining and other related technologies.
Based on current market conditions and the intensity of the drop over the last 24 to 48 hours, Bitcoin Cash and other major cryptocurrencies are expected to drop further in price, with BCHABC eyeing a test of $180 for the first time in its 15-month history.
According to a letter released by the Institute for Business and Social Impact (IBSI), which is to work with the Masters of Financial Engineering (MFE) program at Berkeley, dictates that the grant will finance the faculty, student research and other related activities across the Berkeley Campus.
Its major dominance is in the Asian market especially South Korea, Singapore, and Japan.""".split("\n")

en_test_results = """['P4', ['college'], ['Engineering', 'Law School', 'School of Information']]
['P3', ['fiat deposit'], ['credit card', 'wire', 'bank transfer']]
['P4', ['entity in global financial services ecosystem'], ['crypto market of banks', 'broker dealer', 'exchange', 'payment provider', 'fintechs']]
['P1', ['ten international blockchain standard'], ['terminology', 'concept']]
['P2', ['entity'], ['Securities', 'Exchange Commission']]
['P1', ['famous XRP fan'], ['Michael Arrington', 'co-founder of digital asset management firm Arrington XRP Capital']]
[]
[]
[]
[]
[]
['P3', ['option'], ['Solaris', 'Plan']]
[]
[]
[]
['P4', ['coin'], ['holding', 'BCH']]
['P4', ['related technology'], ['digital coin', 'mining']]
['P4', ['major cryptocurrencies'], ['hour', 'Bitcoin Cash']]
['P4', ['related activity'], ['faculty', 'student research']]
['P5', ['Asian market'], ['South Korea', 'Singapore']]""".split(
        "\n")



en_p = HyponymDetector('en')
@pytest.mark.parametrize(('s', 'r'), zip(en_test_sents, en_test_results))
def test_en_pattern_detector(s,r):
    p = simplify(en_p(s))
    assert repr(p) == r





ru_test_sents = """Северо-восток Сибири и Дальний Восток — регионы преобладания средневысотных горных хребтов, таких как Сихотэ-Алинь, Верхоянский, Черского и т. д. Полуостров Камчатка (здесь находится самый высокий вулкан Евразии Ключевская Сопка (4750 м) и Курильские острова на крайнем востоке — территория вулканов.
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
Многие школы соционики утверждают о неполном соответствии типологии Майерс-Бриггс и соционической типологии, однако считают допустимым использование различных дихотомических тестов, включая различные адаптированные версии опросника Майерс-Бриггс, в качестве одного из инструментов, наряду с другими, для определения соционического типа.""".split("\n")

ru_test_results = """['P1_gent_accs_loct', ['средневысотный горный хребет'], ['сихотэ-алинь', 'верхоянский', 'черский']]
['P4_ablt', ['характеристика'], ['атмосферная циркуляция', 'континентальность климата']]
[]
[]
['P3', ['международная организация'], ['совет европы', 'обсе']]
['P4_nomn', ['страна'], ['страны Евросоюза', 'сша', 'канада', 'великобритания', 'китай', 'япония']]
['P2', ['страна'], ['испания', 'канада', 'мексика', 'индонезия']]
['P4_gent_accs_loct', ['металл'], ['добыча угля', 'нефть', 'газ', 'апатит', 'никель']]
[]
[]
['P4_gent_accs_loct', ['учёных в СССР'], ['курчатов', 'королёв']]
[]
[]
[]
[]""".split("\n")




ru_p = HyponymDetector('ru')
@pytest.mark.parametrize(('s', 'r'), zip(ru_test_sents, ru_test_results))
def test_ru_pattern_detector(s,r):
    p = simplify(ru_p(s))
    assert repr(p) == r


# def test_en_pattern_detector():
#
#     en_p = HyponymDetector('en')
#
#     for s, r in zip(en_test_sents, en_test_results):
#         p = simplify(en_p(s))
#         print(p)
#         # assert repr(p) == r

# def test_ru_pattern_detector():
#
#     ru_p = HyponymDetector('ru')
#
#     for s, r in zip(ru_test_sents, ru_test_results):
#         p = simplify(ru_p(s))
#         print(p)
#         # assert repr(p) == r

# if __name__=="__main__":
#     test_en_pattern_detector()
#     print()
#     test_ru_pattern_detector()