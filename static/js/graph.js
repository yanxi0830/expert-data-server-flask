var svg = d3.select("svg");
var width = +svg.attr("width");
var height = +svg.attr("height");

// var color = d3.scaleOrdinal(d3.schemeCategory20);
var color = d3.scaleSequential().domain([-0.2, 1.2]).interpolator(d3.interpolateViridis);

var link, node, circles, lables;


function updateGraph(nodesSpec) {
    console.log("updateGraph");
    console.log(nodesSpec);

    svg.selectAll("*").remove();

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) { return d.id; }).distance(d => (450 - d.value*5)))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    if (typeof nodesSpec === 'string' || nodesSpec instanceof String) {
        // filepath name
        d3.json(nodesSpec, function (error, graph) {
            if (error) throw error;
            createGraph(graph);
        });
    } else {
        createGraph(nodesSpec);
    }

    function createGraph(graph) {
        console.log("creating graph");
        link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("stroke-width", function (d) { return d.value * 0.05; });

        node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(graph.nodes)
            .enter().append("g")

        circles = node.append("circle")
            .attr("r", 15)
            .attr("fill", function (d) { return color(d.value); })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        lables = node.append("text")
            .text(function (d) {
                return d.id;
            })
            .attr('x', -20)
            .attr('y', 3);

        node.append("title")
            .text(function (d) { return d.id; });

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        function ticked() {
            link
                .attr("x1", function (d) { return d.source.x; })
                .attr("y1", function (d) { return d.source.y; })
                .attr("x2", function (d) { return d.target.x; })
                .attr("y2", function (d) { return d.target.y; });

            node
                .attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")";
                })
        }
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

updateGraph("/static/default_graph.json");