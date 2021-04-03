console.log("Hello CHART")
var originals = [];
dublicated = [];
text = "Maggie. is great";
    if(text.includes("Maggie.")) console.log("We found Maggie");
    d3.json("similarPhoto.json").then(data => {
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
        d3.json("Maggie/Analysis_full/StarterCode/assets/js/filesInfo.json").then(function(data) {
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
      
              var color = d3.scaleOrdinal().domain(data)
                  .range(["pink", "yellow"]);
      
              var canvas = d3
                  .select ("body")
                  .append("svg")
                  .attr("width", 1500)
                  .attr("height", 1500); 
      
              var group = canvas.append("g")
                  .attr("transform", "translate(300, 300)"); 
      
              var arc = d3.arc()
                  .innerRadius(200)
                  .outerRadius(r);
    
      
              var pie = d3.pie()
                  .value(function (d) { return d; });
              
              var arcs = group.selectAll (".arc")
                  .data(pie(data))
                  .enter()
                  .append("g")
                  .attr("class", "arc");
      
              arcs.append("path")
                  .attr("d",arc)
                  .attr("fill", function (d) {return color(d.data); }); 
      
              arcs.append("text")
                  .attr("transform", function (d) { return "translate(" + arc.centroid(d) + ")"; })
                  .attr("text-anchor", "middle")
                  .attr("font-family", "fantasy")
                  .attr("font-size", "1.9 em")
                  .text(function (d) { return d.data; }); 
        
           
            console.log("Original Sizes:", total_size_of_originals);
            console.log("Dublicates Sizes:", total_size_of_dublicates);
        });
        // originalSizes = dublicatedImages.map(d=>d.file_bytes_size)
    });

  
        