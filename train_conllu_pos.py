#%%
from conllu import parse
from pprint import pprint
import pymorphy2
from nltk.tag import _get_tagger, _pos_tag
import pickle

train_path = "/Volumes/External/datasets/Language/Tree Bank/UD/ru/ru_syntagrus-ud-train.conllu"
test_path = "/Volumes/External/datasets/Language/Tree Bank/UD/ru/ru_syntagrus-ud-test.conllu"

FEATURES_OF_INTEREST = [
    'Animacy',
    'Aspect',
    'Case',
    'Gender',
    'Mood',
    'Number',
    'Tense',
    'Voice',
]

m = pymorphy2.MorphAnalyzer()
tagger = _get_tagger('rus')

def read_conllu(path):
    sentences = parse(open(path).read())
    ss = []
    for sentence in sentences:
        s = []

        tokens = [token['form'] for token in sentence]
        nltk_tags = _pos_tag(tokens, 'universal', tagger, 'rus')

        pm_feat = []
        for token, utag in nltk_tags:
            morph_parse = m.parse(token)[0]
            feat = []
            for f in FEATURES_OF_INTEREST:
                attr_val = getattr(morph_parse.tag, f.lower(), "None")
                feat.append(attr_val if attr_val else "None")
            pm_feat.append("_".join([utag] + feat))

        gt_feat = []
        for token in sentence:
            token_form = token['form']
            pos_tag = [token['upostag']]
            if token['feats']:
                feat = [token['feats'].get(f, "None") for f in FEATURES_OF_INTEREST]
            else:
                feat = ["None"]
            gt_feat.append("_".join(pos_tag+feat))

        ss.append(list(zip(tokens, pm_feat, gt_feat)))
    return ss

#%%
# train_sentences = read_conllu(train_path)
# test_sentences = read_conllu(test_path)

train_sentences = pickle.load(open("syntagrus_train.pkl", "rb"))
test_sentences = pickle.load(open("syntagrus_test.pkl", "rb"))

# pickle.dump(train_sentences, open("syntagrus_train.pkl", "wb"))
# pickle.dump(test_sentences, open("syntagrus_test.pkl", "wb"))
# print(test_sentences[:10])

#%%

from nltk.tag import CRFTagger

def crf_feat(tags, index):
    features = []
    if index == 0:
        features.extend(["-"] * (len(FEATURES_OF_INTEREST) + 1))
    else:
        features.extend(tags[index - 1].split("_"))
    features.extend(tags[index].split("_"))
    if index == len(tags) - 1:
        features.extend(["-"] * (len(FEATURES_OF_INTEREST) + 1))
    else:
        features.extend(tags[index + 1].split("_"))
    return features

train_data = []
for sent in train_sentences:
    _, pm_tags, gt_tags = zip(*sent)
    train_data.append(list(zip(pm_tags, gt_tags)))

test_data = []
for sent in test_sentences:
    _, pm_tags, gt_tags = zip(*sent)
    test_data.append(list(zip(pm_tags, gt_tags)))

tagger = CRFTagger(feature_func=crf_feat, verbose=True)
tagger.train(train_data, "tagger_pm_ud.crf")
print(tagger.evaluate(test_data))



