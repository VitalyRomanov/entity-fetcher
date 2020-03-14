# TODO
# 1. Make phrase singular - done
# 2. not all phrases should be singular, need additional classifier
# 3. currently there is only one rule available to inflect phrases
#     it does not work in all cases, e.g. "точка зрения"

class PhraseNormalizer:
    def __init__(self, lang):
        self.normalizer = None
        self.analyzer = None

        if lang == 'en':
            pass
        elif lang == 'ru':
            import pymorphy2 
            self.analyzer = pymorphy2.MorphAnalyzer()

            def normalize(tokens):
                parsed = [self.analyzer.parse(token)[0].inflect({'nomn', 'sing'}) for token in tokens]
                return [analyzed_token.word if analyzed_token is not None else token for analyzed_token, token in zip(parsed, tokens)]
            self.normalizer = normalize

    def __call__(self, phrase):
        if self.normalizer:
            return self.normalizer(phrase)
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