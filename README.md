## Promotion strategy

Assign confidence to edges based on the count. Look at the correctness of the nodes with count 1,2,...,k. When edge with weight 1 is found, assign confidence c[1]. If the edge is found k times, assign confidence c[k]. This beautifully assesses confidence. Needs to be reevaluated every time the extraction process is improved.

0. Normalize entities
0.5 Disambiguate with context, with other subconcepts
1. Unambiguous entites with high count get promoted, rest, receive a confidence score
2. If there is a confident entity among disambiguations, promote it proportionally to the confidence of the original entity. Score down short entities to avoid bias
3. Promote ambiguous entities with respect to the proximity to the unambiguous concepts
4. Promote ambiguous entities with respect to the PMI
5. Extract links. Promote ones with high count.
6. If there are known links inside an extracted pattern, promote low count links as well?


### Given:
List of edges: concepts connected to their respective super concepts. Characteristics of edges:
1. Super-concepts are ambiguous
2. Some super-concepts can appear as sub-concepts
3. The graph is drastically underpopulated
4. Confidence intervals on the majority of data are low

What does not work reliably: 
- word vectors
- because graph is unpopulated, a better candidate for links can appear in the future 

### Need to do:
Resolve ambiguities in graph.

### Thoughts:
1. Some ambiguity can be removed by analyzing the highly connected super-concepts. We can cluster sub-concepts and see which of them form groups. The default strategy is: 
    - assume there are as many uniques super-concepts as given in the edges
    - merge super-concepts based on the co-occurrence of sub-concepts in the hearst patterns
    - look at sub-concepts of highly connected super-concepts, collect information about dependant verbs and adjectives
    - characterize the connected super-concepts using these words
    - do the same for low frequency and sparsely connected nodes. identify whether these are similar to any of aggregated concepts (requires classifier)
2. When there is a sub-concept identical to super-concept, try ot identify context where it appears as sub-concept. If the context matches (use the same classifier as above) with one of the candidates, connect them (need to train carefully). 