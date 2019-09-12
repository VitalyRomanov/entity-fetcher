using LightGraphs, MetaGraphs
using Dates
using JSON
using JLD
using HTTP


struct NamedGraph
    mgraph
    index
    inv_index
end

GRAPH = "graph.jld"

@load GRAPH graph
# graph = JLD.load(GRAPH, "graph")


function all_neighbors(g, v)
    return Set(vcat(outneighbors(g.mgraph, v), inneighbors(g.mgraph, v)))
end

function get_egonet(g, node_name)
    if node_name in keys(g.index)
        node_id = g.index[node_name]
        ego = Set(vcat(neighborhood(g.mgraph, node_id, 2, dir=:in), neighborhood(g.mgraph, node_id, 2, dir=:out)))
        return ego
    else
        return
    end
end

function into_json(g, ego)
    nodes = [Dict("name" => g.inv_index[v]) for v in ego]
    links = []
    for v in ego, n in all_neighbors(g, v)
        e = Edge(v, n)
        if has_edge(g.mgraph, e)
            push!(links, Dict("source" => g.inv_index[e.src], "target" => g.inv_index[e.dst], "type" => get_prop(g.mgraph, e, :type), "count" => get_prop(g.mgraph, e, :count)))
        end
    end

    message = JSON.json(Dict("nodes" => nodes, "links" => links))
    return message
end

function answer_request(g, node_name)
    ego = get_egonet(g, node_name)
    if ego === nothing
        return ""
    else
        return into_json(g, ego)
    end
end

# println(answer_request(graph, "banana"))

HTTP.listen("127.0.0.1", 8081) do http
    println(http.message.target)
    request_str = http.message.target
    # @show http.message
    # @show HTTP.header(http, "Content-Type")
    # while !eof(http)
    #     println("body data: ", String(readavailable(http)))
    # end
    HTTP.setstatus(http, 200)
    HTTP.setheader(http, "Content-Type" => "application/json")
    HTTP.setheader(http, "Access-Control-Allow-Origin" => "*")
    startwrite(http)
    write(http, answer_request(graph, request_str[2:end]))
    # write(http, "response body")
    # write(http, "more response body")
end