console.log("Hello CHART")
d3.json("filesInfo.json").then(function(data) {
    console.log(data)
    var total_size_of_all_files = 0;
    data.forEach((d) => {
        total_size_of_all_files += d.file_bytes_size;
        console.log('I am d for each')
        console.log(d["file_bytes_size"]);
        })

var svgWidth = 800;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// basic svg setup
var svg = d3
  .select("scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// chart group
var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // convert data to numbers
    myData.forEach(function(xdata) {
        xdata.Date = +xdata.Date;
        xdata.Time = +xdata.Time;
        //console.log(xdata.state,xdata.abbr,xdata.age,xdata.healthcare);
    });

    // set x scale function
    var xLinearScale = d3.scaleLinear()
        .domain([d3.min(myData, d=>d.Date)*0.9, 
            d3.max(myData, d => d.age)*1.1])
        .range([0, width]);

    // set y scale function
    var yLinearScale = d3.scaleLinear()
        .domain([0, d3.max(myData, d => d.Time)*1.1])
        .range([height, 0]);

    // axes
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    // append x axis
    chartGroup.append("g")
        .attr("transform", `translate(0, ${height})`)
        .style("font-size", "18px")
        .call(bottomAxis);

    // append y axis
    chartGroup.append("g")
        .style("font-size", "18px")
        .call(leftAxis);
  
    // do the circles
    chartGroup.selectAll("circle")
        .data(myData)
        .enter()
        .append("circle")
        .attr("cx", d => xLinearScale(d.Date))
        .attr("cy", d => yLinearScale(d.Time))
        .attr("r", 12)
        .attr("fill", "orange")
        .attr("opacity", ".3");

    // text in circles
    chartGroup.selectAll("text.text-circles")
        .data(myData)
        .enter()
        .append("text")
        .classed("text-circles",true)
        .text(d => d.abbr)
        .attr("x", d => xLinearScale(d.Date))
        .attr("y", d => yLinearScale(d.Time))
        .attr("dy",5)
        .attr("text-anchor","middle")
        .attr("font-size","12px");

    // y axis
    chartGroup.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 30 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .classed("aText", true)
        .text("Time");

    // x axis
    chartGroup.append("text")
        .attr("y", height + margin.bottom/2 - 10)
        .attr("x", width / 2)
        .attr("dy", "1em")
        .classed("aText", true)
        .text("Date");


});