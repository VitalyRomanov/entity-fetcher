import sys
from collections import Counter
# from  functools import filter

data_path = sys.argv[1]
confidence_threshold = int(sys.argv[2])

def read_pairs():
    for line in open(data_path).read().strip().split("\n"):
        triple = tuple(line.split("\t"))
        yield triple

super_sub = list(read_pairs())

super_c, sub_c = zip(*super_sub)

super_c_count = Counter(super_c)
proper_sup_c = set([key for key in super_c_count if super_c_count[key]>confidence_threshold])

# print("Super: ", len(super_c_count))

# proper_sup_c = list(filter(lambda x: super_c_count[x] > confidence_threshold, super_c_count.keys()))
# sop_cc,_ = zip(*proper_sup_c)
# sop_cc = set(sop_cc)

# print(proper_sup_c[:10])

# print("Proper: ", len(proper_sub_c))

for sup, sub in super_sub:
    if sup in proper_sup_c and sub in proper_sup_c:
        print("%s\t%s" % (sup, sub))