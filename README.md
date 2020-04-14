## Promotion strategy

0. Normalize entities
0.5 Disambiguate with context, with other subconcepts
1. Unambiguous entites with high count get promoted, rest, receive a confidence score
2. If there is a confident entity among disambiguations, promote it proportionally to the confidence of the original entity. Score down short entities to avoid bias
3. Promote ambiguous entities with respect to the proximity to the unambiguous concepts
4. Promote ambiguous entities with respect to the PMI
5. Extract links. Promote ones with high count.
6. If there are known links inside an extracted pattern, promote low count links as well?

## Merging graph

Implement the following procedure
1. For every group of supernodes, identify clusters of subconcepts. 
2. For each cluster create a prototype super concept.
3. Superconcepts probably were mentioned as subconcepts. Identify the best match between prototypes as "super" and as "sub" concepts using vectors. Need to set a threshold