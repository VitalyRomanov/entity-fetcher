import pytest
from PatternDetector import PatternDetector

en_test_sents = """Beautiful Cats such as lion.
Cats such as lion and tiger.
Cats such as lion, tiger, pantera and domestic cat.
Such cats as lions.
Such cats as lions and panteras.
Such cats as lions, tigers and panteras.
Cats including lions.
Cats, including lions.
Cats including lions and panteras.
Cats including lions, tigers and panteras.
Lions and other cats.
Lions, tigers and other cats.
Lions, tigers, panteras and other cats.
Cats, especially lions.
Cats, especially lions and tigers.
Cats, especially lions, tigers and panteras.""".split("\n")

en_test_results = """[Tree('P1', [Tree('NP', [('Beautiful', 'ADJ'), ('Cats', 'NOUN')]), Tree('SRV_such_as', [('such', 'ADJ_such'), ('as', 'ADP_as')]), Tree('NP', [('lion', 'NOUN')])])]
[Tree('P1', [Tree('NP', [('Cats', 'NOUN')]), Tree('SRV_such_as', [('such', 'ADJ_such'), ('as', 'ADP_as')]), Tree('NP', [('lion', 'NOUN')]), ('and', 'CONJ_and'), Tree('NP', [('tiger', 'NOUN')])])]
[Tree('P1', [Tree('NP', [('Cats', 'NOUN')]), Tree('SRV_such_as', [('such', 'ADJ_such'), ('as', 'ADP_as')]), Tree('NP', [('lion', 'NOUN')]), (',', '._,'), Tree('NP', [('tiger', 'NOUN')]), (',', '._,'), Tree('NP', [('pantera', 'NOUN')]), ('and', 'CONJ_and'), Tree('NP', [('domestic', 'ADJ'), ('cat', 'NOUN')])])]
[Tree('P2', [('Such', 'ADJ_such'), Tree('NP', [('cats', 'NOUN')]), ('as', 'ADP_as'), Tree('NP', [('lions', 'NOUN')])])]
[Tree('P2', [('Such', 'ADJ_such'), Tree('NP', [('cats', 'NOUN')]), ('as', 'ADP_as'), Tree('NP', [('lions', 'NOUN')]), ('and', 'CONJ_and'), Tree('NP', [('panteras', 'NOUN')])])]
[Tree('P2', [('Such', 'ADJ_such'), Tree('NP', [('cats', 'NOUN')]), ('as', 'ADP_as'), Tree('NP', [('lions', 'NOUN')]), (',', '._,'), Tree('NP', [('tigers', 'NOUN')]), ('and', 'CONJ_and'), Tree('NP', [('panteras', 'NOUN')])])]
[Tree('P3', [Tree('NP', [('Cats', 'NOUN')]), ('including', 'VERB_including'), Tree('NP', [('lions', 'NOUN')])])]
[Tree('P3', [Tree('NP', [('Cats', 'NOUN')]), (',', '._,'), ('including', 'VERB_including'), Tree('NP', [('lions', 'NOUN')])])]
[Tree('P3', [Tree('NP', [('Cats', 'NOUN')]), ('including', 'VERB_including'), Tree('NP', [('lions', 'NOUN')]), ('and', 'CONJ_and'), Tree('NP', [('panteras', 'NOUN')])])]
[Tree('P3', [Tree('NP', [('Cats', 'NOUN')]), ('including', 'VERB_including'), Tree('NP', [('lions', 'NOUN')]), (',', '._,'), Tree('NP', [('tigers', 'NOUN')]), ('and', 'CONJ_and'), Tree('NP', [('panteras', 'NOUN')])])]
[Tree('P4', [Tree('NP', [('Lions', 'NOUN')]), Tree('SRV_and_other', [('and', 'CONJ_and'), ('other', 'ADJ_other')]), Tree('NP', [('cats', 'NOUN')])])]
[Tree('P4', [Tree('NP', [('Lions', 'NOUN')]), (',', '._,'), Tree('NP', [('tigers', 'NOUN')]), Tree('SRV_and_other', [('and', 'CONJ_and'), ('other', 'ADJ_other')]), Tree('NP', [('cats', 'NOUN')])])]
[Tree('P4', [Tree('NP', [('Lions', 'NOUN')]), (',', '._,'), Tree('NP', [('tigers', 'NOUN')]), (',', '._,'), Tree('NP', [('panteras', 'NOUN')]), Tree('SRV_and_other', [('and', 'CONJ_and'), ('other', 'ADJ_other')]), Tree('NP', [('cats', 'NOUN')])])]
[Tree('P5', [Tree('NP', [('Cats', 'NOUN')]), (',', '._,'), ('especially', 'ADV_especially'), Tree('NP', [('lions', 'NOUN')])])]
[Tree('P5', [Tree('NP', [('Cats', 'NOUN')]), (',', '._,'), ('especially', 'ADV_especially'), Tree('NP', [('lions', 'NOUN')]), ('and', 'CONJ_and'), Tree('NP', [('tigers', 'NOUN')])])]
[Tree('P5', [Tree('NP', [('Cats', 'NOUN')]), (',', '._,'), ('especially', 'ADV_especially'), Tree('NP', [('lions', 'NOUN')]), (',', '._,'), Tree('NP', [('tigers', 'NOUN')]), ('and', 'CONJ_and'), Tree('NP', [('panteras', 'NOUN')])])]""".split(
        "\n")



en_p = PatternDetector('en', backend='nltk')
@pytest.mark.parametrize(('s', 'r'), zip(en_test_sents, en_test_results))
def test_en_pattern_detector(s, r):
    p = en_p(s)
    assert repr(p) == r


ru_test_sents = """Кошки такие как слоны и носороги.
Такие кошки как слоны и носороги.
Кошки, включая слонов и носорогов.
Слоны, носороги и другие кошки.
Кошки, особенно слоны и носороги.
Кошки, в частности слоны и носороги.""".split("\n")

ru_test_results = """[Tree('P1_nomn', [Tree('NP_noun', [('Кошки', 'NOUN_gent_femn_sing')]), Tree('SRV_takie_kak', [('такие', 'PRON_такие'), ('как', 'CONJ_как')]), Tree('NP_noun', [('слоны', 'NOUN_nomn_masc_plur')]), ('и', 'CONJ_и'), Tree('NP_noun', [('носороги', 'NOUN_nomn_masc_plur')])])]
[Tree('P2', [('Такие', 'PRON_такие'), Tree('NP_noun', [('кошки', 'NOUN_gent_femn_sing')]), ('как', 'CONJ_как'), Tree('NP_noun', [('слоны', 'NOUN_nomn_masc_plur')]), ('и', 'CONJ_и'), Tree('NP_noun', [('носороги', 'NOUN_nomn_masc_plur')])])]
[Tree('P3', [Tree('NP_noun', [('Кошки', 'NOUN_gent_femn_sing')]), (',', '._,'), ('включая', 'ADP_включая'), Tree('NP_noun', [('слонов', 'NOUN_gent_masc_plur')]), ('и', 'CONJ_и'), Tree('NP_noun', [('носорогов', 'NOUN_gent_masc_plur')])])]
[Tree('P4_nomn', [Tree('NP_noun', [('Слоны', 'NOUN_nomn_masc_plur')]), (',', '._,'), Tree('NP_noun', [('носороги', 'NOUN_nomn_masc_plur')]), Tree('SRV_i_drygiye', [('и', 'CONJ_и'), ('другие', 'PRON_другие')]), Tree('NP_noun', [('кошки', 'NOUN_gent_femn_sing')])])]
[Tree('P5', [Tree('NP_noun', [('Кошки', 'NOUN_gent_femn_sing')]), (',', '._,'), ('особенно', 'ADV_особенно'), Tree('NP_noun', [('слоны', 'NOUN_nomn_masc_plur')]), ('и', 'CONJ_и'), Tree('NP_noun', [('носороги', 'NOUN_nomn_masc_plur')])])]
[Tree('P6', [Tree('NP_noun', [('Кошки', 'NOUN_gent_femn_sing')]), (',', '._,'), Tree('SRV_v_chasnosti', [('в', 'ADP_в'), ('частности', 'NOUN_loct_femn_sing_частности')]), Tree('NP_noun', [('слоны', 'NOUN_nomn_masc_plur')]), ('и', 'CONJ_и'), Tree('NP_noun', [('носороги', 'NOUN_nomn_masc_plur')])])]""".split("\n")


ru_p = PatternDetector('ru', backend='nltk')
@pytest.mark.parametrize(('s', 'r'), zip(ru_test_sents, ru_test_results))
def test_ru_pattern_detector(s, r):
    p = ru_p(s)
    assert repr(p) == r





# def test_en_pattern_detector():
#
#     from PatternDetector import PatternDetector
#
#     en_p = PatternDetector('en', backend='nltk')
#
#     for s, r in zip(en_test_sents, en_test_results):
#         print(en_p(s)[0])
#         assert repr(en_p(s)) == r

# def test_ru_pattern_detector():
#
#     from PatternDetector import PatternDetector
#
#     ru_p = PatternDetector('ru', backend='nltk')
#
#     for s, r in zip(ru_test_sents, ru_test_results):
#         print(ru_p(s)[0])
#         assert repr(ru_p(s)) == r


# if __name__=="__main__":
#     test_en_pattern_detector()
#     print()
#     test_ru_pattern_detector()