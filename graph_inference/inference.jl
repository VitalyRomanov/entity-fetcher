using Revise
using Embeddings
using LinearAlgebra

EMBEDDINGS_FILE = "/home/ltv/data/models/embeddings/crawl-300d-2M.vec"

# TODO
# 1. word2vec does not give desired results
# 2. it fails the most with low frequency concepts. in some cases
#       it is evident that a comcept belongs to the superconcept,
#       but word2vec assigns the lowes score to this concept-superconcept
#       pair
# 3. it seems that the analysis of the additional information is needed to
#       correctly dentify relevant superconcept. We can use verbs and adjectives
#       for this.
# 4. When trying to connect the taxonomy, we often have a situation where
#       we have soem subconcepts with different meaning. This means that the
#       concept has several prototypes. In return, the concept also has its
#       parents. These are superconcepts. We need to understand how to connect
#       subconcepts to corresponding superconcepts. The problem is that for some
#       of the subconcepts we may have not yet encountered any relevant superconcepts,
#       or vice versa. This makes the problem much more complex because the
#       number of classes is now unconstrained. We need more general understanding
#       of the language to solve this problem.
# 5. For now disambiguate concepts, leave taxonomy linking for the future.
# 6. Try adding new PATTERN_NEIGH_TYPE links using word2vec

include("build_graph.jl")

emb_table = load_embeddings(FastText_Text, EMBEDDINGS_FILE)

graph = build_graph()

visited = Set()

function filter_edges_by_type(edges, type)
    (edge for edge in edges if edge[:type] == type)
end

const get_word_index = Dict(word=>ii for (ii,word) in enumerate(emb_table.vocab))

function embed(line)
    global emb_table
    words = split(line)

    words = [word for word in words if word in keys(get_word_index)]

    if length(words) > 0
        inds = [get_word_index[word] for word in words]
        emb = sum(emb_table.embeddings[:,ind] for ind in inds)
        return emb
    else
        return zeros(300)
    end
end

function process_senses(graph, concept, senses)
    println("\nConcept: $concept, senses: $(length(senses))")

    sense_emb = zeros(length(senses), 300)
    for (ind, sense) in enumerate(senses)
        for sub_concept in sense
            sense_emb[ind, :] += embed(sub_concept)
        end

        sense_emb[ind, :] = normalize(sense_emb[ind, :])
        # sense_emb[ind, :] = normalize(sense_emb[ind, :] + embed(concept))
    end

    parents = [e[:src] for e in filter_edges_by_type(inedges(graph, concept), HAS_A_TYPE)]

    println("Parents: $parents")
    println("Senses: $senses")
    for parent in parents
        parent_emb = embed(parent)

        inner = hcat([normalize(sense_emb[ind, :]).*normalize(parent_emb) for ind in 1:size(sense_emb)[1]]...)

        # println("$(size(sum(inner, dims=1)))")
        probs = sum(inner, dims=1)[:]
        probs = exp.(probs * 4)
        # probs = [if prob > 0.; prob else 0.; end for prob in probs]
        probs /= sum(probs)
        # println("$(size(probs))")
        for (ind, _) in enumerate(senses)
            println("Membership for $parent -> $(senses[ind]): $(probs[ind])")
        end
    end

end

for seed_edge in edges(graph)

    if seed_edge[:src] in visited; continue; end

    ne = filter_edges_by_type(outedges(graph, seed_edge[:src]), HAS_A_TYPE)

    chld = [e[:dst] for e in ne]

    if length(chld) == 0; continue; end

    # println(seed_edge[:src], chld)

    senses = connected_components(graph[chld])

    if length(senses) > 1
        # println(senses)
        process_senses(graph, seed_edge[:src], senses)
    end

    push!(visited, seed_edge[:src])


end
