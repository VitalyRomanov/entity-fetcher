import re
import sys
import argparse
from collections import Counter

from py2neo import Relationship
from py2neo.ogm import Repository

from fetcher.HyponymExtractor import HyponymDetector
from LanguageTools.wrappers.nltk_wrapper import Sentencizer
import hashlib
import json

from fetcher.datamodel import Sentence, HearstPattern, Concept


def pattern_id(pattern):
    return hashlib.md5(repr(pattern).encode('utf-8')).hexdigest()


def get_pre_labels(candidates, s):
    labels = []
    for c in candidates:
        for match in re.finditer(c["super"]["candidates"][0], s):
            start, stop = match.span()
            labels.append([start, stop, "SUP"])
            break
        for sub in c["sub"]:
            for match in re.finditer(sub["candidates"][0], s):
                start, stop = match.span()
                labels.append([start, stop, "SUB"])
                break
        break


# def create_candidates(graph, candidates, mentioned_in):
#     cand = []
#
#     for name in candidates["candidates"]:
#         c = graph.get(Concept, primary_value=name)
#         if c is None:
#             c = Concept(type=candidates["type"], name=name)
#         c.mentioned_in.add(mentioned_in)
#         cand.append(c)
#
#
#     candidates = cand
#     # candidates = [Concept(type=candidates["type"], name=name, mentioned_in=mentioned_in) for name in
#     #           candidates["candidates"]]
#
#     for c1 in candidates:
#         for c2 in candidates:
#             if c1 is c2:
#                 continue
#             c1.conflicting_with.add(c2)
#
#     return candidates
#
#
# def create_pattern(graph, pattern, sent):
#     g_pattern = HearstPattern(id=pattern_id(pattern), type=pattern["type"])
#
#     super_candidates = create_candidates(graph, pattern["super"], sent)
#
#     sub_candidates = []
#     for sub in pattern["sub"]:
#         sub_candidates.extend(create_candidates(graph, sub, sent))
#
#     for sup in super_candidates:
#         for sub in sub_candidates:
#             g_pattern.sub_candidates.add(sub)
#             sub.is_a.add(sup)
#
#     for sup in super_candidates:
#         g_pattern.super_candidates.add(sup)
#
#     for sub in sub_candidates:
#         g_pattern.sub_candidates.add(sub)
#
#
#     # subgraph = g_pattern
#     # for node in chain(super_candidates, sub_candidates):
#     #     subgraph = subgraph | node
#
#     return g_pattern, super_candidates, sub_candidates


def create_candidates(graph, candidates, mentioned_in):
    cand = []
    edges = []

    for name in candidates["candidates"]:
        c = Concept(type=candidates["type"], name=name)
        edges.append(Relationship(c, "mentioned_in", mentioned_in))
        cand.append(c)


    candidates = cand
    # candidates = [Concept(type=candidates["type"], name=name, mentioned_in=mentioned_in) for name in
    #           candidates["candidates"]]

    for c1 in candidates:
        for c2 in candidates:
            if c1 is c2:
                continue
            edges.append(Relationship(c1, "conflicting_with", c2))

    return candidates, edges


def create_pattern(graph, pattern, sent):
    edges = []
    g_pattern = HearstPattern(id=pattern_id(pattern), type=pattern["type"])

    super_candidates, edges_ = create_candidates(graph, pattern["super"], sent)
    edges.extend(edges_)

    sub_candidates = []
    for sub in pattern["sub"]:
        sub_candidates_, edges_ = create_candidates(graph, sub, sent)
        sub_candidates.extend(sub_candidates_)
        edges.extend(edges_)

    for sup in super_candidates:
        for sub in sub_candidates:
            edges.append(Relationship(g_pattern, "sub_candidates", sub))
            edges.append(Relationship(sub, "is_a", sup))

    for sup in super_candidates:
        edges.append(Relationship(g_pattern, "super_candidates", sup))

    for sub in sub_candidates:
        edges.append(Relationship(g_pattern, "sub_candidates", sub))


    subgraph = None
    for edge in edges:
        if subgraph is None:
            subgraph = edge
        else:
            subgraph = subgraph | edge

    return subgraph


def main():
    parser = argparse.ArgumentParser(description='Train word vectors')
    parser.add_argument('language', type=str, default='en', help='Language: English or Russian')
    parser.add_argument('--password', "-p", dest="password", type=str, default='', help='')
    args = parser.parse_args()

    if args.language == 'en':
        LANG = 'english'
        LANG_CODE = 'en'
    elif args.language == 'ru':
        LANG = 'russian'
        LANG_CODE = 'ru'
    else:
        raise ValueError("This language is not supported:", args.language)

    sentencizer = Sentencizer(LANG)


    hyp = HyponymDetector(LANG_CODE)


    dump_files = {
        'P1':open("concepts_p1.txt", "w"),
        'P2':open("concepts_p2.txt", "w"),
        'P3':open("concepts_p3.txt", "w"),
        'P4':open("concepts_p4.txt", "w"),
        'P5':open("concepts_p5.txt", "w"),
        'P6':open("concepts_p6.txt", "w"),
        'P7':open("concepts_p7.txt", "w")
    }

    # graph = Graph("bolt://neo4j@localhost:7687", password=args.password)
    graph = Repository("bolt://neo4j@localhost:7687", password=args.password)

    sentense_bank = open("sentense_bank.txt", "w")
    recorded_sentences = set()

    concepts = Counter()
    count = 0

    print("******************")
    print("Ready to extract")
    print("******************")

    def sentence_id(sentence):
        return hashlib.md5(sentence.encode('utf-8')).hexdigest()


    def lowercase_first(sentence):
        if len(sentence) > 1 and sentence[1].lower() == sentence[1]:
            return sentence[0].lower() + sentence[1:]
        else:
            return sentence

    candidate_count = 0

    for line in sys.stdin:
        if line:

            try:
                line = " ".join(json.loads(line)['text'].split("\n"))
            except:
                pass

            for s in sentencizer(line):
                s = lowercase_first(s)
                candidates = hyp(s)

                if candidates:
                    sentence_record = {
                        "sent_id": sentence_id(s),
                        "text": s,
                    }
                    # g_sent = Sentence(id=sentence_id(s), content=s)



                    sentense_bank.write("%s\n" % json.dumps(sentence_record, ensure_ascii=False))
                    # recorded_sentences.add(sentence_id)
                    for c in candidates:

                        # subgraph = create_pattern(graph, c, g_sent)
                        ## graph.save(g_sent, pattern, *super_c, *sub_c)
                        # graph.merge(subgraph)

                        c['sent_id'] = sentence_record['sent_id']
                        dump_files[c['type'][:2]].write("%s\n" % json.dumps(c, ensure_ascii=False))

                        candidate_count += 1
                        if candidate_count % 10000 == 0:
                            print("Found %d candidates" % candidate_count)

if __name__ == "__main__":
    main()