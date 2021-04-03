console.log("Hello CHART")
var g = svg.append("g")
                   .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        var color = d3.scaleOrdinal(['#4daf4a','#377eb8','#ff7f00','#984ea3','#e41a1c']);

        var pie = d3.pie().value(function(d) { 
                return d.percent; 
            });

        var path = d3.arc()
                     .outerRadius(radius - 10)
                     .innerRadius(0);

        var label = d3.arc()
                      .outerRadius(radius)
                      .innerRadius(radius - 80);
// d3.select("body").on("load", function(){
    var originals = [];
    dublicated = [];
    text = "Maggie. is great";
        if(text.includes("Maggie.")) console.log("We found Maggie");
    
    d3.json("static/json/similarPhoto.json").then(data => {
        Object.entries(data).forEach(([k,v]) => {
            originals.push(k);
            dublicated = dublicated.concat(v);
            console.log(originals);

            // console.log(k);
        });
        var unique = dublicated.filter((v1,i1,a1)=>a1.indexOf(v1)===i1);
        console.log(originals);
        console.log("originals:", originals.length);
        console.log("dublicated:", dublicated.length);
        console.log("dublicated unique:", unique.length);
        var originalImages = []
        var dublicatedImages = []
        var total_size_of_originals=0;
        var total_size_of_dublicates=0;
        d3.json("static/json/filesInfo.json").then(function(data) {
            console.log(data)
            var total_size_of_all_files = 0;
            data.forEach((d) => {
                unique.forEach(a=>{
                    if(d["file_id"].includes(a+".")) {
                        total_size_of_originals += d.file_bytes_size;
                        // console.log("Original image "+a);
                        // originalImages.push(d);
                    }else{
                        total_size_of_dublicates += d.file_bytes_size;
                        // console.log("Dublicated image "+a);
                        // dublicatedImages.push(d);

                    }
                });
               total_size_of_all_files += d.file_bytes_size;
            //    console.log(d);
              //   console.log('I am d for each')
              //   console.log(d["file_bytes_size"]);
              })


              total_size_mega = (Math.round (total_size_of_originals/1000000));
              total_size_dup_mega = (Math.round (total_size_of_dublicates/1000000));
              var data = [total_size_mega, total_size_dup_mega]
              var r = 300; 

              var svg = d3.select("svg"),
            width = svg.attr("width"),
            height = svg.attr("height"),
            radius = Math.min(width, height) / 2;
        
        

        
            var arc = g.selectAll(".arc")
                       .data(pie(data))
                       .enter().append("g")
                       .attr("class", "arc");

            arc.append("path")
               .attr("d", path)
               .attr("fill",  'yellow');
        
            console.log(arc)
        
            arc.append("text")
               .attr("transform", function(d) { 
                        return "translate(" + label.centroid(d) + ")"; 
                })
               .text(function(d) { return d.data.browser; });
            });

            svg.append("g")
               .attr("transform", "translate(" + (width / 2 - 120) + "," + 20 + ")")
               .append("text")
               .text("Browser use statistics - Jan 2017")
               .attr("class", "title")
        });
        // originalSizes = dublicatedImages.map(d=>d.file_bytes_size)
    });

// })
        