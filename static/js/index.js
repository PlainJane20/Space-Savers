d3.select("#get_images").on("change", function() {
    d3.json("/file_extraction").then(function(filesData) {
        console.log(filesData);
    });
});