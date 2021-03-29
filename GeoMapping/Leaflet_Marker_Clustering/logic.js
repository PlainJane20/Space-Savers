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


// Use this link to get the geojson data.
//var link = "Analysis_Neighborhoods.geojson";
//var url = "[https://data.sfgov.org/resource/g8m3-pdis.json]"


d3.json(url, function(response) {

  console.log(response);
  var markers = L.markerClusterGroup();
  response.forEach(element => {
    var location = element.location;
console.log(location);
    // Check for location property
    if (location) {
      console.log("Hey, it works!");
      // Add a new marker to the cluster group and bind a pop-up
   
    markers.addLayer(L.marker([location.coordinates[1], location.coordinates[0]])
    .bindPopup("<h1>" + element.dba_name + "</h1> <hr> <h3>Neighborhood: " + element.neighborhoods_analysis_boundaries + "</h3>")).addTo(myMap) ;
}

});
});