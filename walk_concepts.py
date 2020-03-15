import json
import sys
import pymorphy2

m = pymorphy2.MorphAnalyzer()

def analyze(phrase):
    parsed = [m.parse(p)[1] for p in phrase]
    return [(p.tag.POS, p.tag.case, p.tag.gender, p.tag.number) for p in parsed]


def iterate_concepts(concept):
    yield concept['super']['candidates'][0].split()
    for c in concept['sub']:
        yield c['candidates'][0].split()

for line in sys.stdin:
    try:
        concept = json.loads(line)
        for c in iterate_concepts(concept):
            if len(c)> 1:
                # a =
                print(*c, sep="\t")
                # print(*c, *analyze(c), sep="\t")
    except:
        continue