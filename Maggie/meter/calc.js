
d3.json("C:\Users\Javier\Desktop\SS_ma\Maggie\meter\filesInfo.json", function(data) {
    data.forEach(d, function(d) {
        total_size_of_all_files += d.file_bytes_size;
        console.log(d);