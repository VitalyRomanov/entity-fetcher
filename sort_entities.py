from collections import Counter
import sys

data_path = sys.argv[1]

def read_pairs():
    for line in open(data_path).read().strip().split("\n"):
        yield tuple(line.split("\t"))

allp = [(pair[0], pair[1], count) for pair, count in Counter(read_pairs()).most_common()]

# allp.sort(key=lambda x:x[0])

with open("to_boris.tsv", "w") as tb:
    for r in allp:
        tb.write("%s\t%s\t%d\n" % (r))


