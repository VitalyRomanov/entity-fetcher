using LightGraphs, MetaGraphs

struct NamedGraph
    mgraph::MetaDiGraph
    index::Dict
    inv_index::Dict
end

NamedGraph() = begin 
    NamedGraph(MetaDiGraph(), Dict(), Dict())
end

function Base.getindex(graph::NamedGraph, node_key::Any, node_prop::Any)
    node_id = graph.index[node_key]
    return get_prop(graph.mgraph, node_id, Symbol(node_prop))
end

function Base.getindex(graph::NamedGraph, edge::Tuple, edge_prop::Any)
    node_id1 = graph.index[edge[1]]
    node_id2 = graph.index[edge[2]]

    e = Edge(node_id1, node_id2)

    return get_prop(graph.mgraph, e, Symbol(edge_prop))
end

function Base.setindex!(graph::NamedGraph, value::Any, node_key::Any, node_prop::Any)
    node_id = graph.index[node_key]
    return set_prop!(graph.mgraph, node_id, Symbol(node_prop), value)
end

function Base.setindex!(graph::NamedGraph, value::Any, edge::Tuple, edge_prop::Any)
    node_id1 = graph.index[edge[1]]
    node_id2 = graph.index[edge[2]]

    e = Edge(node_id1, node_id2)

    return set_prop!(graph.mgraph, e, Symbol(edge_prop), value)
end

function add_node!(graph::NamedGraph, node_name)
    if node_name in keys(graph.index)
        return false
    else
        added = add_vertex!(graph.mgraph, Dict(:name => node_name))
        if added
            graph.index[node_name] = nv(graph.mgraph)
            graph.inv_index[nv(graph.mgraph)] = node_name
        end
        return added
    end
end

function add_node!(graph::NamedGraph, node_name, props::Dict)
    added = add_node!(graph, node_name)
    if added
        for kv in props
            graph[node_name, kv[1]] = kv[2]
        end
    end
    return added
end


# import LightGraphs.SimpleGraphs.add_edge!
function MetaGraphs.add_edge!(graph::NamedGraph, edge::Tuple)
    node_id1 = graph.index[edge[1]]
    node_id2 = graph.index[edge[2]]
    e = Edge(node_id1, node_id2)

    if has_edge(graph.mgraph, e)
        return false
    else
        return add_edge!(graph.mgraph, node_id1, node_id2)
    end
end

function LightGraphs.SimpleGraphs.add_edge!(graph::NamedGraph, edge::Tuple, props::Dict)
    added = add_edge!(graph, edge)
    node_id1 = graph.index[edge[1]]
    node_id2 = graph.index[edge[2]]
    e = Edge(node_id1, node_id2)

    if added
        for kv in props
            graph[e, kv[1]] = kv[2]
        end
    end
end

# import MetaGraphs.props
function MetaGraphs.props(graph::NamedGraph, node_key)
    node_id = graph.index[node_key]
    return props(graph.mgraph, node_id)
end

function props(graph::NamedGraph, edge::Tuple)
    node_id1 = graph.index[edge[1]]
    node_id2 = graph.index[edge[2]]

    e = Edge(node_id1, node_id2)

    return props(graph.mgraph, e)
end

function Base.getindex(graph::NamedGraph, node_key)
    # node_id = graph.index[node_key]
    return props(graph, node_key)
end

function Base.getindex(graph::NamedGraph, edge::Tuple)
    # node_id = graph.index[node_key]
    return props(graph, edge)
end

function Base.in(node, graph::NamedGraph)
    return node in keys(graph.index)
end

function decode_edge(graph, edge_src, edge_dst)
    return merge(
        Dict(
            :src => graph.inv_index[edge_src], 
            :dst => graph.inv_index[edge_dst]
            ), 
        MetaGraphs.props(
            graph.mgraph, Edge(edge_src, edge_dst)
        )
    )
end

function edges(graph::NamedGraph) 
    function decode_edge(edge)
        return merge(Dict(:src => graph.inv_index[edge.src], :dst => graph.inv_index[edge.dst]), MetaGraphs.props(graph.mgraph, edge))
    end
    return (decode_edge(edge) for edge in MetaGraphs.edges(graph.mgraph))
end

function outneighbors(graph::NamedGraph, node_key)
    node_id = graph.index[node_key]

    return (graph.inv_index[node] for node in MetaGraphs.outneighbors(graph.mgraph, node_id))
end

function outedges(graph::NamedGraph, node_key)
    node_id = graph.index[node_key]
    neighborhood = MetaGraphs.outneighbors(graph.mgraph, node_id)

    (decode_edge(graph, node_id, n) for n in neighborhood)
end

function induced_subgraph(graph::NamedGraph, nodes::Array)
    query_nodes = [graph.index[n] for n in nodes]
    
    subgraph, vmap = MetaGraphs.induced_subgraph(graph.mgraph, query_nodes)

    sub_index = Dict()
    sub_inv_index = Dict()

    for v in 1:nv(subgraph)
        sub_index[get_prop(subgraph, v, :name)] = v
        sub_inv_index[v] = get_prop(subgraph, v, :name)
    end

    NamedGraph(subgraph, sub_index, sub_inv_index)
end

function MetaGraphs.connected_components(graph::NamedGraph)
    components = MetaGraphs.connected_components(graph.mgraph)

    return [[graph.inv_index[node] for node in group] for group in components]
end

function Base.getindex(graph::NamedGraph, nodes::Array)
    induced_subgraph(graph, nodes)
end