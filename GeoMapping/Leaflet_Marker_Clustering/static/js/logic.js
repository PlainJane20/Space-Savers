// Creating map object

var myMap = L.map("map", {
  center: [37.7749, -122.4194],
  zoom: 11
});
console.log("Hello");
// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);


// read JSON file
var url = "static/js/filesInfo.json";
console.log(url);

d3.json(url, function(response) {
console.log(response);
  // Create a new marker cluster group
  var markers = L.markerClusterGroup();
  response.forEach(element => {
    var coordinates = element.coordinates;

    // Check for location property
    if (coordinates.length == 2) {
      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([coordinates[0], coordinates[1]])
      .bindPopup("<h1>" + element.file_id + "</h1> <hr> <h3>Date: " + element.Date + "</h3>" + "</h1> <hr> <h3>Time: " + element.Time + "</h3>"
          + "</h1> <hr> <h3>Taken with a " + element.madeBy + " " + element.model + "</h3>"));
    } 

  });
  markers.addTo(myMap);

});