import spacy

class SpacyWrapper:
    def __init__(self, language):
        self.lang_code = language
        self.model = 'en_core_web_md' if language=='en' else '/Users/LTV/Desktop/model-final-ner-rich-morph-120it'

        self.nlp = spacy.load(self.model)
        # self.nlp.disable_pipes('parser')

    def __call__(self, text):
        tags = []
        doc = self.nlp(text)

        if self.lang_code == 'en':
            parsed_ents = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.noun_chunks]
        elif self.lang_code == 'ru':
            parsed_ents = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents if ent.label_ == "NP"]
        else:
            raise NotImplementedError()

        parsed = spacy.gold.biluo_tags_from_offsets(doc, parsed_ents)
        for t, tag in zip(doc, parsed):
            # tags.append((t.text, t.pos_, t.tag_, tag))
            tags.append((t.text, tag))
        # for s in doc.sents:
        #     tags.append([])
        #     for t, tag in zip(s, parsed):
        #         tags[-1].append((t.text, t.pos_, t.tag_, tag))
        # sents = self.sentencize(text)
        # t_sents = [self.tokenize(sent) for sent in sents]
        # tags = [self.tag(t_sent) for t_sent in t_sents]
        # from nltk import pos_tag

        # tags = [pos_tag(sent, tagset='universal') for sent in sents]
        return tags

    def noun_chunks(self, text):
        return self(text)

if __name__=="__main__":
    from pprint import pprint
    nlp_en = SpacyWrapper("en")
    # text_en = "Alice's Adventures in Wonderland (commonly shortened to Alice in Wonderland) is an 1865 novel written by English author Charles Lutwidge Dodgson under the pseudonym Lewis Carroll.[1] It tells of a young girl named Alice falling through a rabbit hole into a fantasy world populated by peculiar, anthropomorphic creatures."
    text_en = "Bitcoin.com, Roger Ver, Bitmain, and other members of the opposing camp have yet to publicly weigh in with a response as of the time of writing, but — given that Bitcoin ABC has already been labeled “Bitcoin Cash” by most exchanges and other crypto services — it’s unlikely that they’ll agree to his terms."
    tags_en = nlp_en(text_en)
    pprint(tags_en)

    # nlp_ru = SpacyWrapper("ru")
    # text_ru = "«Приключения Алисы в Стране чудес» (англ. Alice’s Adventures in Wonderland), часто используется сокращённый вариант «Алиса в Стране чудес» (англ. Alice in Wonderland) — сказка, написанная английским математиком, поэтом и прозаиком Чарльзом Лютвиджем Доджсоном под псевдонимом Льюис Кэрролл и изданная в 1865 году. В ней рассказывается о девочке по имени Алиса, которая попадает сквозь кроличью нору в воображаемый мир, населённый странными антропоморфными существами."
    # tags_ru = nlp_ru(text_ru)
    # pprint(tags_ru)