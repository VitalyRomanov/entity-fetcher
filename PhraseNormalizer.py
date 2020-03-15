# TODO
# 1. Make phrase singular - done
# 2. not all phrases should be singular, need additional classifier
# 3. currently there is only one rule available to inflect phrases
#     it does not work in all cases, e.g. "точка зрения"
# 4. There are a lot of issues with feninine phrases

en_proc_stop_words = {'of', 'in', 'with', 'for', 'on', 'throughout', 'over'}

def normalize_en(tokens, type, analyzer):
    process = True
    normalized_tokens = []
    for t in tokens:
        if t in en_proc_stop_words:
            process = False
        if process:
            normalized_tokens.append(analyzer.lemmatize(t))
        else:
            normalized_tokens.append(t)
    return normalized_tokens

    # return [analyzer.lemmatize(t) for t in tokens]

PROPER_NOUN = {'NOUN'}
PROPER_ADJ = {'ADJF', 'ADJS'}

def ru_select_proper_parse(parse, pos):
    for p in parse:
        if p.tag.POS in pos:
            return p
    return parse[0]

def normalize_ru(tokens, ent_type, analyzer):

    # TODO
    # probably need to process exceptions for phrases that
    # should remain plural

    if ent_type == "NP_adj_noun_q" or ent_type == "NP_adj_noun":

        parsed = [analyzer.parse(token) for token in tokens]

        parsed = [ru_select_proper_parse(p, PROPER_ADJ)
                  if ind != len(parsed)-1 else
                  ru_select_proper_parse(p, PROPER_NOUN)
                  for ind, p in enumerate(parsed)]

        gender = parsed[-1].tag.gender

        if gender is None:
            for p in parsed:
                if p.tag.gender is not None:
                    gender = p.tag.gender
                    break

        morph = {'nomn', 'sing'}
        if gender is not None:
            morph.add(gender)

        inflected = [i.word if i is not None else par.word for par, i in
                     zip(parsed, (p.inflect(morph) for p in parsed))]
        # inflected = [p.inflect(morph).word for p in parsed]
        return inflected

    if ent_type == "NP_noun_noun_q" or ent_type == "NP_noun_noun":
        # TODO
        # This rule does not work properly when both nouns have case 'gent'
        # Probably need to generate both options for such NP and score them with
        # W2V. Basically, need coherence classifier here.
        parsed = [analyzer.parse(token) for token in tokens]
        parsed = [ru_select_proper_parse(p, PROPER_NOUN)
                  for p in parsed]

        morph = {'gent', 'sing'}

        inflected = [i.word if i is not None else par.word for par, i in
                     zip(parsed, (p.inflect(morph) for p in parsed))]
        # inflected = [p.inflect(morph) for p in parsed]
        i = parsed[0].inflect({'nomn', 'sing'})
        inflected[0] = i.word if i is not None else parsed[0].word
        return inflected

    # if ent_type == "NP_noun_noun_s":
    #     parsed = [analyzer.parse(token) for token in tokens]
    #     parsed = [ru_select_proper_parse(p, PROPER_NOUN)
    #               for p in parsed]
    #
    #     morph = {'nomn', 'sing'}
    #
    #     inflected = [i.word if i is not None else par.word for par, i in
    #                  zip(parsed, (p.inflect(morph) for p in parsed))]
    #     return inflected

    if ent_type == "NP_noun":
        parsed = ru_select_proper_parse(
            analyzer.parse(tokens[0]),
            PROPER_NOUN
        )

        i = parsed.inflect({'sing', 'nomn'})

        return [i.word if i is not None else parsed.word]

    if ent_type == "NP_adj":
        parsed = ru_select_proper_parse(
            analyzer.parse(tokens[0]),
            PROPER_ADJ
        )

        i = parsed.inflect({'sing', 'nomn'})

        return [i.word if i is not None else parsed.word]

    return tokens

    # parsed = [analyzer.parse(token)[0] for token in tokens]
    #
    # morph = []
    #
    # noun_gend = None
    # default_case = 'nomn'
    #
    # for ind, p in enumerate(parsed):
    #     morph.append({'sing', default_case})
    #
    #     if p.tag.POS == "NOUN":
    #         if noun_gend is None:
    #             noun_gend = p.tag.gender
    #
    #     if p.tag.POS == "NOUN":
    #         default_case = 'gent'
    #
    # if noun_gend is not None:
    #     for m, p in zip(morph, parsed):
    #         if p.tag.POS in {'ADJF', 'ADJS'}:
    #             m.add(noun_gend)
    #
    # # print(morph)
    #
    # inflected = [p.inflect(m) for m,p in zip(morph, parsed)]
    # return [analyzed_token.word if analyzed_token is not None else token for analyzed_token, token in zip(inflected, tokens)]

class PhraseNormalizer:
    def __init__(self, lang):
        self.normalizer = None
        self.analyzer = None

        if lang == 'en':
            from nltk.stem import WordNetLemmatizer
            self.analyzer = WordNetLemmatizer()
            self.normalizer = normalize_en
        elif lang == 'ru':
            import pymorphy2 
            self.analyzer = pymorphy2.MorphAnalyzer()
            self.normalizer = normalize_ru

    def __call__(self, phrase, type):
        if self.normalizer:
            return self.normalizer(phrase, type, self.analyzer)
        else:
            return phrase

if __name__ == "__main__":
    phrases = [
        ("тротиловом","эквиваленте"),
        ("программного","обеспечения"),
        ("Персидского","залива"),
        ("тихий","океан"),
        ("Виктор","Янукович"),
        ("Валентина","Матвиенко"),
        ("североатлантический","альянс"),
        ("точку","зрения"),
        ("марий","эл"),
        ("Дальний","Восток"),
        ("мевлютый","чавушогла"),
        ("внешнеполитического","ведомства"),
        ("экономического","форума"),
        ("главного","редактора"),
        ("боевых","действиях")
    ]

    ru_norm = PhraseNormalizer("ru")

    for phrase in phrases:
        print(ru_norm(phrase))