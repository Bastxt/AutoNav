{
    //Make an SVG Container
    var max = 500;
    var min = 0;

    var car_pos = [
        { "x": 100, "y": 100 },
        { "x": 200, "y": 200 },
        { "x": 300, "y": 300 },
        { "x": 400, "y": 400 },
        { "x": 500, "y": 500 }
    ];

    var lidar = () => [
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
        { "x_axis": Math.random() * (max - min) + min, "y_axis": Math.random() * (max - min) + min },
    ];

    var margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = 600 - margin.left - margin.right,
        height = 640 - margin.top - margin.bottom;

    var svg = d3.select("div#container")
        .append("svg")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", '0 0 810 610')
        .style("border-color", "black")
        .style("border-style", "solid")
        .style("border-width", "1px")
        .style("padding", "15px")
        .classed("svg-content", true);

    // Add X axis --> it is a date format
    var x = d3.scaleLinear()
        .domain([0, 500])
        .range([1, 800]);

    var y = d3.scaleLinear()
        .domain([0, 500])
        .range([600, 0]);

    svg.append("g")
        .attr("transform", "translate(0,600)")
        .call(d3.axisTop(x));

    svg.append("g")
        .attr("transform", "translate(0,0)")
        .call(d3.axisRight(y));


    var dots = svg.selectAll("dots")
        .data(lidar)
        .enter()
        .append("circle");

    var car = svg.selectAll("car")
        .data(car_pos)
        .enter()
        .append("circle");

    // gridlines in y axis function
    function make_y_gridlines() {
        return d3.axisLeft(y)
            .ticks(10)
    }

    // gridlines in y axis function
    function make_x_gridlines() {
        return d3.axisBottom(x)
            .ticks(10)
    }


    // add the y gridlines
    svg.append("g")
        .attr("class", "grid")
        .call(make_y_gridlines()
            .tickSize(-width * 2)
            .tickFormat("")
        )

    svg.append("g")
        .attr("class", "grid")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_gridlines()
            .tickSize(-height)
            .tickFormat("")
        )

    function sleep(ms) {
        return new Promise(
            resolve => setTimeout(resolve, ms)
        );
    }

    function update() {
        dots.data(lidar);
        dots.transition().duration(500)
            .attr("cx", function (d) { return x(d.x_axis) })
            .attr("cy", function (d) { return y(d.y_axis) })
            .attr("r", 5)
            .style("fill", "#69b3a2");

        car.data(car_pos);
        
        car.transition().duration(500)
            .attr("cx", function (d) { return x(d.x_axis) })
            .attr("cy", function (d) { return x(d.x_axis) })
            .attr("r", 30)
            .style("fill", "#66BB6A");
    }

    setInterval(update, 500);
}