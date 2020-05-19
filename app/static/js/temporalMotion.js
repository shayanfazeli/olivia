function plot_parsed_data(data) {
    //data = FileAttachment(path_to_json_dataset).json();
    var x_var = "census_poverty";
    var y_var = "confirmed_count_cumsum";
    var size_var = "death_count_cumsum";

    bisectDay = d3.bisector(([day]) => day).left;


    margin = ({top: 20, right: 20, bottom: 35, left: 40});
    height = 560;
    width = 700;

    x = d3.scaleLinear([0, 60], [margin.left, width - margin.right]);
    y = d3.scaleLinear([0, 10000], [height - margin.bottom, margin.top]);
    radius = d3.scaleSqrt([0, 10e8], [0, width / 24]);
    color = d3.scaleOrdinal(data.map(d => d.state), d3.schemeCategory10).unknown("black");

    xAxis = g => g
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(width / 80, ","))
        .call(g => g.select(".domain").remove())
        .call(g => g.append("text")
            .attr("x", width)
            .attr("y", margin.bottom - 4)
            .attr("fill", "currentColor")
            .attr("text-anchor", "end")
            .text(x_var))

    yAxis = g => g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .call(g => g.select(".domain").remove())
        .call(g => g.append("text")
            .attr("x", -margin.left)
            .attr("y", 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text(y_var))

    grid = g => g
        .attr("stroke", "currentColor")
        .attr("stroke-opacity", 0.1)
        .call(g => g.append("g")
            .selectAll("line")
            .data(x.ticks())
            .enter().append("line")
            .attr("x1", d => 0.5 + x(d))
            .attr("x2", d => 0.5 + x(d))
            .attr("y1", margin.top)
            .attr("y2", height - margin.bottom))
        .call(g => g.append("g")
            .selectAll("line")
            .data(y.ticks())
            .enter().append("line")
            .attr("y1", d => 0.5 + y(d))
            .attr("y2", d => 0.5 + y(d))
            .attr("x1", margin.left)
            .attr("x2", width - margin.right));


    // var svg = d3.select("#my_palette")
    //     .attr("viewBox", [0, 0, width, height]);


    var svg = d3.select("#my_palette")
        .attr("viewBox", [0, 0, width, height]);

    svg.append("g")
        .call(xAxis);

    svg.append("g")
        .call(yAxis);

    svg.append("g")
        .call(grid);

    var x_vars = [];
    for (obj in data){
        x_vars.push(obj[x_var]);
    }
    console.log("shayan" + data[0][x_var]);
    console.log(x_vars[3]);

    var circle = svg.append("g").attr("stroke", "black")
        .selectAll("circle")
        .data(dataAt(90), d => d.county)
        .enter().append("circle")
        .sort((a, b) => d3.descending(a[size_var], b[size_var]))
        .attr("cx", d => x(d[x_var]))
        .attr("cy", d => y(d[y_var]))
        .attr("r", d => radius(d[size_var] * 100.0))
        .attr("fill", d => color(d.state))
        .call(circle => circle.append("title")
            .text(d => [d.county, d["state"]].join("\n")));

    function new_svg(svg, data) {

        Object.assign(svg.node(), {
            update(data) {
                circle.data(data, d => d.county)
                    .sort((a, b) => d3.descending(a[size_var], b[size_var]))
                    .attr("cx", d => x(d[x_var]))
                    .attr("cy", d => y(d[y_var]))
                    .attr("r", d => radius(d[size_var]));
            }
        });

        svg.node().update(data);
    }

    function dataAt(day) {
        return data.map(d => ({
            county: d.county,
            state: d.state,
            x_var: valueAt(d[x_var], day),
            size_var: valueAt(d[size_var], day),
            y_var: valueAt(d[y_var], day)
        }));
    }

    function valueAt(values, day) {
        const i = bisectDay(values, day, 0, values.length - 1);
        const a = values[i];
        if (i > 0) {
            const b = values[i - 1];
            const t = (day - a[0]) / (b[0] - a[0]);
            return a[1] * (1 - t) + b[1] * t;
        }
        return a[1];
    }


    currentData = dataAt(80);
    // chart.update(currentData);
    svg = new_svg(svg, currentData);




}

/* Copyright for the core code is 2020 Observable, Inc. , altered by ER Lab*/

