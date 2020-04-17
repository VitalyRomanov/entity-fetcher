include("build_graph.jl")

graph = build_graph()

visited = Set()

function filter_edges_by_type(edges, type)
    (edge for edge in edges if edge[:type] == type)
end

for seed_edge in edges(graph)

    if seed_edge[:src] in visited; continue; end

    ne = filter_edges_by_type(outedges(graph, seed_edge[:src]), HAS_A_TYPE)

    chld = [e[:dst] for e in ne]

    if length(chld) == 0; continue; end

    # println(seed_edge[:src], chld)

    senses = connected_components(graph[chld])

    if length(senses) > 1
        println(senses)
    end

    push!(visited, seed_edge[:src])


end