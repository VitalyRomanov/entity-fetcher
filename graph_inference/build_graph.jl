using LightGraphs, MetaGraphs
using Dates
using JSON
using JLD

include("NamedGraph.jl")
include("LanguageTools.jl")

lt = LanguageTools

PARKING_LOT = "parking_lot.txt"
GRAPH = "graph.jld"

NORMAL_TYPE = "normal"
HAS_A_TYPE = "has_a"
PATTERN_NEIGH_TYPE = "pattern_neighbour"


function build_graph()

    # en_lemm = LanguageTools.load("en_lemma.dict")

    # if isfile(PARKING_LOT)
    #     parking_lot = open(PARKING_LOT, "a")
    # else
    #     parking_lot = open(PARKING_LOT, "w")
    # end

    if isfile(GRAPH)
        @load GRAPH graph
    else
        graph = NamedGraph()
    end


    function is_ambiguous(pattern)
        # if length(pattern["super"]) > 1 || any(length(sub) > 1 for sub in pattern["sub"])
        #     return true
        # end
        return false
    end


    function get_super(pattern)
        # return pattern["super"]["candidates"][1]
        return pattern["super"][1]
    end


    function get_sub(pattern)
        return [sub[1] for sub in pattern["sub"]]
        # return [sub["candidates"][1] for sub in pattern["sub"]]
        # return vcat(pattern["sub"]...)
    end


    function normalize(concept)
        # n_concept = join([LanguageTools.remove_accents(LanguageTools.lemmatize(en_lemm, word)) for word in LanguageTools.tokenize(concept)], " ")
        n_concept = lt.remove_accents(concept)
        return n_concept
    end

    add_and_count!(graph, node) = begin
        if add_node!(graph, node)
            graph[node, "count"] = 1
        else
            graph[node, "count"] += 1
        end
    end

    add_and_count_edge_with_type!(graph, node1, node2, type) = begin
        edge = (node1, node2)
        if add_edge!(graph, edge)
            graph[edge, "count"] = 1
            graph[edge, "type"] = type
        else
            graph[edge, "count"] += 1
        end
    end



    count = 0

    println("Begin")

    for line in eachline(stdin)

        if length(strip(line)) > 0
            pattern = JSON.parse(line)

            if is_ambiguous(pattern)
                # write(parking_lot, "$line\n")
                nothing
            else
                sup = get_super(pattern)
                # sup_normal_form = normalize(sup)

                add_and_count!(graph, sup)

                sub_c = get_sub(pattern)

                for concept in sub_c
                    add_and_count!(graph, concept)
                    add_and_count_edge_with_type!(graph, sup, concept, HAS_A_TYPE)
                end

                for concept in sub_c, neigh in sub_c
                    if concept != neigh 
                        add_and_count_edge_with_type!(graph, concept, neigh, PATTERN_NEIGH_TYPE)
                    end
                end


            end
        end

        count = count + 1
        if count % 10000 == 0
            println("$(Dates.now()) Processed $count facts")
        end
    end


    # close(parking_lot)
    return graph
end

# build_graph()


