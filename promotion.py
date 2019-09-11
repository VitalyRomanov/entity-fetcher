import json
import sys

import os
import spacy
import networkx as nx
import pickle
from collections import Counter

import matplotlib.pyplot as plt

import datetime
from time import time
from numba import jit



language = sys.argv[1]
# graph_location = sys.argv[2] if len(sys.argv) > 2 else "%s_graph.pkl" % language
counters_location = sys.argv[3] if len(sys.argv) > 3 else "%s_counters.pkl" % language
# pending_location = sys.argv[4] if len(sys.argv) > 4 else ""
# normalization_graph

# if os.path.isfile(graph_location):
#     graph = pickle.load(graph_location, "rb")
# else:
#     graph = nx.DiGraph()

if os.path.isfile(counters_location):
    concepts, normal_forms = pickle.load(counters_location, "rb")
else:
    concepts, normal_forms = Counter(), Counter()

# if os.isfile(pending_location):
#     pending


# class GraphExtender:
#     def init(graph, concept_counter, normal_counter):
#         self.graph = graph
#         self.concept_counter = concept_counter
#         self.normal_counter = normal_counter
# expander = GraphExtender(graph, concepts, normal_forms)


print("=============")
print("Loading Spacy")
print("=============")
if language == 'en':
    spacy_nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser"])
else:
    pass
print("=====done====")
print("=============")

parking_lot = []
accepted = []

parking_lot = open("parking_lot.txt", "w")

def normalize(concept):
    return concept
    doc = spacy_nlp(concept)
    # return "".join([t.lemma_ + t.whitespace_ for t in doc])
    lemmatized = " ".join([t.lemma_ for t in doc])
    return lemmatized.lower()

def is_ambiguous(pattern):
    if len(pattern['super']) > 1 or any(len(sub) > 1 for sub in pattern['sub']):
        return True
    return False

def get_links(patter):
    for sub in pattern['sub']:
        yield (patter['super'], sub)  
    # return (patter['super'], sub)  

# def get_concepts(pattern):
def increment_counter(counter, item):
    if item in counter:
        counter[item] += 1
    else:
        counter.item = 1
    
def get_super(pattern):
    for sup in pattern['super']:
        yield sup

def get_sub(pattern):
    for subs in pattern['sub']:
        for sub in subs:
            yield sub

def add_node(graph, node):
    if graph.has_node(node):
        c_count = nx.classes.function.get_node_attributes(graph, 'count')[node]
        nx.classes.function.set_node_attributes(graph, {node: {'count': c_count + 1}})
    else:
        graph.add_node(node, count=1)

def add_edge(graph, edge, type):
    if graph.has_edge(edge[0], edge[1]):
        attributes = nx.classes.function.get_edge_attributes(graph, 'count')
        if edge in attributes:
            c_count = attributes[edge]
            nx.classes.function.set_edge_attributes(graph, {edge: {'count': c_count + 1}})
        return
    graph.add_edge(edge[0], edge[1], type=type, count=1)


count = 0

# normalization_graph = nx.DiGraph()
# isa_graph = nx.DiGraph()
# neighbour_graph = nx.Graph()
graph = nx.Graph()

for line in sys.stdin:
    if line.strip():
        pattern = json.loads(line)

        if is_ambiguous(pattern):
            pass
            # parking_lot.write(line)
        else:
            sup = list(get_super(pattern))[0]
            sup_normal_form = normalize(sup)

            add_node(graph, sup)
            add_node(graph, sup_normal_form)

            add_edge(graph, (sup, sup_normal_form), "normal")

            sub_c = list(get_sub(pattern))

            for concept in get_sub(pattern):
                normal_form = normalize(concept)
                add_node(graph, concept)
                add_node(graph, normal_form)
                add_edge(graph, (concept, normal_form), "normal")
                add_edge(graph, (sup_normal_form, normal_form), "has_a")

            for concept in get_sub(pattern):
                normal_form = normalize(concept)
                
                for neigh in sub_c:
                    neigh_normal_form = normalize(neigh)
                    if neigh_normal_form == normal_form: continue
                    add_edge(graph, (normal_form, neigh_normal_form), "pattern_neighbour")

    count += 1
    if count % 200 == 0:
        st = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        print("%s Processed %d facts" % (st, count))
    #     break
            # accepted.extend(get_links(pattern))

# print(normal_forms)
# print(neighbour_graph['country'])
# nx.classes.function.set_node_attributes(graph, {'service':{'count':1}})
# print(list(e for e in graph.edges(data=True)))
pickle.dump("graph.pkl", graph)
sys.exit()

print()

for concept, count in normal_forms.most_common():
    if count < 3: continue
    subg = neighbour_graph.subgraph(nx.generators.ego.ego_graph(isa_graph, concept, center=False, undirected=False).nodes())
    cc = list(nx.algorithms.components.connected_components(subg))
    n_cliques = len(cc)
    debug = [list(c) for c in cc] if n_cliques > 1 else ""
    

    # n_cliques = nx.number_of_cliques(neighbour_graph, concept)
    # n_cliques = nx.square_clustering(neighbour_graph, concept)
    # debug = nx.cliques_containing_node(neighbour_graph, concept) if n_cliques > 2 else []
    # debug = "|".join(neighbour_graph[concept].keys()) if n_cliques > 2 else ""
    print("{}\t{}\t{}\t{}".format(concept, count, n_cliques, debug))

# plt.rcParams['text.usetex'] = False

# normal_count = Counter(normal_form)
# original_count = Counter()
# plt.figure(figsize=(8, 8))
# try:
#     # pos = nx.nx_agraph.graphviz_layout(normalization_graph)
#     pos = nx.nx_agraph.graphviz_layout(normalization_graph, prog='twopi', args='')
# except:
#     pos = nx.spring_layout(normalization_graph, iterations=20)

# nx.draw_networkx_edges(normalization_graph, pos, alpha=0.3, edge_color='m')
# nx.draw_networkx_nodes(normalization_graph, pos, node_color='w', alpha=0.4)
# nx.draw_networkx_labels(normalization_graph, pos, fontsize=4)

# G = normalization_graph
# pos = nx.spring_layout(G)
# nx.draw(G, pos, font_size=16, with_labels=False)
# for p in pos:  # raise text positions
#     pos[p][1] += 0.07
# nx.draw_networkx_labels(G, pos)

# nx.draw(normalization_graph) 
# plt.show()
# plt.savefig("1.svg")
